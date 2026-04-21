"""
generate_review_report.py
Converts golden_set.jsonl into a readable Markdown report data/review_dataset.md.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent
GOLDEN_FILE = DATA_DIR / "golden_set.jsonl"
VECTOR_FILE = DATA_DIR / "vector_db.json"
REPORT_FILE = DATA_DIR / "review_dataset.md"

def main():
    if not GOLDEN_FILE.exists():
        print(f"Error: {GOLDEN_FILE} not found.")
        return

    # Load Vector DB for source info if needed
    chunk_map = {}
    if VECTOR_FILE.exists():
        vdb = json.loads(VECTOR_FILE.read_text(encoding="utf-8"))
        chunk_map = {c["chunk_id"]: c for c in vdb}

    # Load Golden Set
    cases = []
    with GOLDEN_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            cases.append(json.loads(line))

    # Generate Markdown
    md = "# 📋 Manual Review: Golden Dataset (70 cases)\n\n"
    md += "> [!IMPORTANT]\n"
    md += "> Please review the Q/A pairs, ground truth IDs, and sources below.\n"
    md += "> Mark incorrect cases for correction.\n\n"
    
    md += "| # | Question | Expected Answer | Ground Truth ID | Source | Diff |\n"
    md += "|---|---|---|---|---|---|\n"
    
    for i, c in enumerate(cases, 1):
        gid = c.get("ground_truth_id", "")
        source = chunk_map.get(gid, {}).get("source", "N/A")
        diff = c.get("difficulty", "medium")
        
        q = c.get("question", "").replace("|", "\\|")
        a = c.get("expected_answer", "").replace("|", "\\|")
        if len(a) > 150: a = a[:147] + "..."
        
        md += f"| {i} | {q} | {a} | {gid} | {source} | {diff} |\n"

    REPORT_FILE.write_text(md, encoding="utf-8")
    print(f"Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    main()
