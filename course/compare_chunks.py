import json
import statistics

def analyze_file(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lengths = [len(d.get("chunk", "")) for d in data]
    return {
        "file": file,
        "n_chunks": len(data),
        "avg_length": round(statistics.mean(lengths), 1) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
    }

if __name__ == "__main__":
    files = [
        "faq_chunks_sliding.json",
        "faq_chunks_paragraphs.json",
        "faq_chunks_sections.json"
    ]

    results = [analyze_file(f) for f in files]

    print("\n=== Résumé comparatif des chunks ===")
    for r in results:
        print(
            f"{r['file']}: {r['n_chunks']} chunks | "
            f"moyenne {r['avg_length']} caractères "
            f"(min {r['min_length']}, max {r['max_length']})"
        )
