"""
synthetic_gen.py — AI-Powered Golden Dataset Generator (Lab 14)
================================================================
"""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
    load_dotenv(Path(__file__).parent.parent / "day08" / "lab" / ".env")
except ImportError:
    pass

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
LLM_PROVIDER:   str = os.getenv("LLM_PROVIDER", "openai").lower()

_BASE        = Path(__file__).parent.parent
DOCS_DIR     = _BASE / "day08" / "lab" / "data" / "docs"
OUT_VECTOR   = Path(__file__).parent / "vector_db.json"
OUT_GOLDEN   = Path(__file__).parent / "golden_set.jsonl"

TARGET_TOTAL = 70

def build_vector_db() -> List[Dict]:
    all_chunks = []
    if not DOCS_DIR.exists(): return []
    for fpath in sorted(DOCS_DIR.glob("*.txt")):
        text = fpath.read_text(encoding="utf-8")
        lines = text.splitlines()
        meta = {"source": "", "department": ""}
        for ln in lines[:8]:
            if ln.startswith("Source:"): meta["source"] = ln[7:].strip()
            if ln.startswith("Department:"): meta["department"] = ln[11:].strip()
        
        parts = re.split(r"===\s*(.+?)\s*===", text)
        for i in range(1, len(parts) - 1, 2):
            body = parts[i + 1].strip()
            if body:
                all_chunks.append({
                    "chunk_id": f"{fpath.stem}_c{len(all_chunks)+1}",
                    "source": meta["source"],
                    "section": parts[i].strip(),
                    "text": body
                })
    return all_chunks

def build_prompt(chunks: List[Dict], counts: Dict[str, int]) -> str:
    chunks_json = json.dumps([{"id": c["chunk_id"], "txt": c["text"][:500]} for c in chunks], ensure_ascii=False)
    total = sum(counts.values())
    return f"""Create {total} RAG test cases in Vietnamese using these chunks: {chunks_json}.
Distribution: {json.dumps(counts)}
Format: JSON array of objects. Each object MUST have:
"question", "expected_answer", "ground_truth_id", "expected_retrieval_ids" (list), "difficulty" (easy/medium/hard/multi_hop), "type" (standard/adversarial/edge_case), "category".
ONLY return the JSON array."""

async def call_ai(prompt: str, provider: str) -> str:
    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = await asyncio.get_event_loop().run_in_executor(None, lambda: model.generate_content(prompt))
        return resp.text
    else:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return resp.choices[0].message.content

def parse_json(raw: str) -> List[Dict]:
    # Robust numeric find
    match = re.search(r"\[\s*\{.*\}\s*\]", raw, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: pass
    
    # Try direct parse if match fails
    try:
        data = json.loads(raw)
        if isinstance(data, list): return data
        if isinstance(data, dict):
            for k in ["cases", "data", "test_cases"]:
                if k in data and isinstance(data[k], list): return data[k]
    except: pass
    return []

BATCH_CONFIG = [
    ("SLA", ["sla_p1_2026"], {"easy": 4, "medium": 4, "hard": 2, "multi_hop": 2, "adversarial": 1}),
    ("Refund", ["policy_refund_v4"], {"easy": 4, "medium": 3, "hard": 2, "multi_hop": 2, "adversarial": 2}),
    ("Access", ["access_control_sop"], {"easy": 4, "medium": 3, "hard": 2, "multi_hop": 2, "adversarial": 1}),
    ("HR", ["hr_leave_policy"], {"easy": 3, "medium": 3, "hard": 2, "multi_hop": 2, "adversarial": 2}),
    ("IT", ["it_helpdesk_faq"], {"easy": 3, "medium": 3, "hard": 2, "multi_hop": 2, "adversarial": 0}),
    ("Cross", ["sla", "access", "refund", "hr", "it"], {"medium": 2, "hard": 3, "multi_hop": 3, "adversarial": 2})
]

async def main():
    print("Building VectorDB...")
    vdb = build_vector_db()
    vdb_ids = {c["chunk_id"] for c in vdb}
    
    all_cases = []
    for domain, stems, counts in BATCH_CONFIG:
        batch_chunks = [c for c in vdb if any(s.lower() in c["chunk_id"].lower() for s in stems)]
        if not batch_chunks:
            print(f"No chunks for {domain}")
            continue
        
        print(f"Generating {domain} batch...")
        raw = await call_ai(build_prompt(batch_chunks, counts), LLM_PROVIDER)
        cases = parse_json(raw)
        print(f"  Received {len(cases)} cases from AI")
        
        # Grounding check
        for c in cases:
            if c.get("ground_truth_id") in vdb_ids:
                all_cases.append(c)

    print(f"Total valid cases collected: {len(all_cases)}")
    
    # Save
    with open(OUT_GOLDEN, "w", encoding="utf-8") as f:
        for c in all_cases[:TARGET_TOTAL]:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
            
    with open(OUT_VECTOR, "w", encoding="utf-8") as f:
        json.dump(vdb, f, ensure_ascii=False, indent=2)
        
    print(f"Done! Saved {min(len(all_cases), TARGET_TOTAL)} cases to {OUT_GOLDEN}")

if __name__ == "__main__":
    asyncio.run(main())
