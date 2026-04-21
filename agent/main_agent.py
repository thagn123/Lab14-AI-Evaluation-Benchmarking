"""
agent/main_agent.py - RAG Agent sử dụng Ollama local LLM (qwen2.5:0.5b)

V1 (Base):    Dense retrieval + random noise → retrieval sai → LLM trả lời sai
V2 (Optimized): Hybrid BM25+Dense+RRF retrieval đúng → LLM trả lời đúng, grounded

Model: qwen2.5:0.5b chạy local qua Ollama (~400MB RAM)
Fallback: Nếu Ollama chưa ready, dùng template answer từ context.
"""
import asyncio
import json
import os
import random
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# VectorDB loader
# ---------------------------------------------------------------------------
_DB_PATH = Path(__file__).parent.parent / "data" / "vector_db.json"

def _load_db() -> List[Dict]:
    try:
        return json.loads(_DB_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []

VECTOR_DB: List[Dict] = _load_db()
CHUNK_MAP: Dict[str, Dict] = {c["chunk_id"]: c for c in VECTOR_DB}


# ---------------------------------------------------------------------------
# Tokenizer (Vietnamese-friendly BM25 simulation)
# ---------------------------------------------------------------------------
def _tok(text: str) -> List[str]:
    return re.findall(r"\w+", text.lower())


def _bm25(query_tokens: List[str], doc_text: str, k1: float = 1.5, b: float = 0.75) -> float:
    doc_tokens = _tok(doc_text)
    if not doc_tokens:
        return 0.0
    avgdl = 120  # estimated average chunk length in tokens
    score = 0.0
    tf_map: Dict[str, int] = {}
    for t in doc_tokens:
        tf_map[t] = tf_map.get(t, 0) + 1
    dl = len(doc_tokens)
    for qt in set(query_tokens):
        tf = tf_map.get(qt, 0)
        if tf == 0:
            continue
        idf = 1.0  # simplified (no corpus-level IDF)
        score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
    return score


# ---------------------------------------------------------------------------
# Retrieval strategies
# ---------------------------------------------------------------------------
def _dense_retrieve(query: str, top_k: int = 5) -> List[Dict]:
    """Keyword overlap ranking (simulated dense retrieval)."""
    tokens = _tok(query)
    ranked = sorted(VECTOR_DB, key=lambda c: _bm25(tokens, c["text"]), reverse=True)
    return ranked[:top_k]


def _sparse_retrieve(query: str, top_k: int = 5) -> List[Dict]:
    """Exact n-gram match (sparse keyword retrieval)."""
    q_lower = query.lower()
    # Extract meaningful keywords (≥3 chars)
    keywords = [w for w in _tok(query) if len(w) >= 3]
    scored = []
    for c in VECTOR_DB:
        hits = sum(1 for kw in keywords if kw in c["text"].lower())
        scored.append((hits, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


def _hybrid_rrf(query: str, top_k: int = 3, rrf_k: int = 60) -> List[Dict]:
    """
    Hybrid Retrieval: Dense + Sparse results fused via Reciprocal Rank Fusion.
    """
    dense = _dense_retrieve(query, top_k=10)
    sparse = _sparse_retrieve(query, top_k=10)

    scores: Dict[str, float] = {}
    for rank, c in enumerate(dense):
        cid = c["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank + 1)
    for rank, c in enumerate(sparse):
        cid = c["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank + 1)

    top_ids = sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
    return [CHUNK_MAP[cid] for cid in top_ids if cid in CHUNK_MAP]


def _random_retrieve(top_k: int = 3) -> List[Dict]:
    """
    V1 random baseline: picks random chunks regardless of query.
    Simulates a broken/naive retriever for regression testing.
    """
    pool = VECTOR_DB.copy()
    random.shuffle(pool)
    return pool[:top_k]


# ---------------------------------------------------------------------------
# Ollama LLM interface
# ---------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:0.5b"


def _ollama_available() -> bool:
    try:
        req = urllib.request.Request("http://localhost:11434/")
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        return False


def _call_ollama(prompt: str, timeout: int = 60) -> str:
    """
    Call local Ollama API (non-streaming).
    Returns the generated text or raises if unavailable.
    """
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 256}
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "").strip()


def _build_prompt(question: str, context_chunks: List[Dict], version: str) -> str:
    """Build a grounded RAG prompt from context chunks."""
    context_block = ""
    for i, c in enumerate(context_chunks, 1):
        context_block += (
            f"\n[{i}] Nguồn: {c['source']} | Mục: {c['section']}\n"
            f"{c['text']}\n"
        )

    if version == "V2":
        instruction = (
            "Bạn là trợ lý nội bộ IT/CS. "
            "Chỉ trả lời dựa trên các đoạn văn bản được cung cấp bên dưới. "
            "Nếu thông tin không có trong tài liệu, hãy nói rõ rằng bạn không biết. "
            "Trích dẫn nguồn tài liệu khi trả lời."
        )
    else:
        # V1: prompt lỏng lẻo, không ép grounding → dễ hallucinate
        instruction = (
            "Bạn là một trợ lý AI thông minh. "
            "Hãy trả lời câu hỏi sau dựa trên kiến thức của bạn."
        )

    return (
        f"{instruction}\n\n"
        f"### Tài liệu tham khảo:\n{context_block}\n"
        f"### Câu hỏi:\n{question}\n\n"
        f"### Câu trả lời:"
    )


def _fallback_answer(question: str, chunks: List[Dict], version: str) -> str:
    """
    Fallback khi Ollama chưa start: trả lời dựa trên nội dung chunk.
    V2 trích dẫn nguồn, V1 trả lời mơ hồ.
    """
    if not chunks:
        return "Tôi không tìm thấy thông tin liên quan trong tài liệu hiện tại."

    best = chunks[0]
    snippet = best["text"][:300]

    if version == "V2":
        return (
            f"Dựa trên tài liệu [{best['source']}] — {best['section']}:\n"
            f"{snippet}..."
        )
    else:
        # V1: câu trả lời thiếu context, không grounded
        return f"Theo thông tin tôi có: {snippet[:150]}..."


# ---------------------------------------------------------------------------
# MainAgent class
# ---------------------------------------------------------------------------
class MainAgent:
    """
    RAG Agent với 2 chế độ:
      V1 (Base):       Random retrieval → bad context → poor/hallucinated answer
      V2 (Optimized):  Hybrid RRF retrieval → correct context → grounded answer

    LLM backend: Ollama qwen2.5:0.5b (local, ~400MB)
    Fallback: template-based answer nếu Ollama chưa khởi động.
    """

    def __init__(self, version: str = "V1"):
        self.version = version
        self.name = f"SupportAgent-{version}"
        self._ollama_ok: Optional[bool] = None  # cached check

    def _check_ollama(self) -> bool:
        if self._ollama_ok is None:
            self._ollama_ok = _ollama_available()
            if not self._ollama_ok:
                print(
                    f"  [Agent {self.version}] Ollama not running - "
                    "using fallback mode. Run: ollama serve && ollama pull qwen2.5:0.5b"
                )
        return self._ollama_ok

    async def query(self, question: str) -> Dict:
        await asyncio.sleep(0.01)  # yield control

        # --- Retrieval ---
        if self.version == "V1":
            # V1: 60% correct retrieval, 40% random → simulates naive dense-only retriever
            if random.random() < 0.40:
                chunks = _random_retrieve(top_k=3)
            else:
                chunks = _dense_retrieve(question, top_k=3)
        else:
            # V2: Hybrid RRF (always uses best available retrieval)
            chunks = _hybrid_rrf(question, top_k=3)

        retrieved_ids = [c["chunk_id"] for c in chunks]

        # --- Generation ---
        use_ollama = self._check_ollama()

        if use_ollama:
            try:
                prompt = _build_prompt(question, chunks, self.version)
                loop = asyncio.get_event_loop()
                answer = await loop.run_in_executor(None, _call_ollama, prompt)
            except Exception as e:
                print(f"  [Ollama error] {e} — using fallback")
                answer = _fallback_answer(question, chunks, self.version)
        else:
            answer = _fallback_answer(question, chunks, self.version)

        context_texts = [c["text"] for c in chunks]
        context_block = "\n---\n".join(
            f"[{c['source']} | {c['section']}]\n{c['text'][:200]}"
            for c in chunks
        )

        return {
            "answer": answer,
            "retrieved_ids": retrieved_ids,
            "contexts": context_texts,
            "metadata": {
                "model": OLLAMA_MODEL if use_ollama else "fallback",
                "version": self.version,
                "tokens_used": len(context_block.split()) + len(question.split()),
                "sources": list({c["source"] for c in chunks}),
                "ollama_used": use_ollama,
            },
        }


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    async def _test():
        print("=== V2 (Hybrid) ===")
        agent_v2 = MainAgent(version="V2")
        r = await agent_v2.query("Ticket P1 có SLA phản hồi ban đầu là bao lâu?")
        print("Retrieved:", r["retrieved_ids"])
        print("Answer:", r["answer"][:300])
        print()
        print("=== V1 (Random/Dense) ===")
        agent_v1 = MainAgent(version="V1")
        r1 = await agent_v1.query("Ticket P1 có SLA phản hồi ban đầu là bao lâu?")
        print("Retrieved:", r1["retrieved_ids"])
        print("Answer:", r1["answer"][:300])

    asyncio.run(_test())
