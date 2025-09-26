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
import json
import os
from openai import OpenAI
from tqdm import tqdm

# Initialiser le client OpenAI
openai_client = OpenAI(api_key="ta_nouvelle_cle_api")

# Prompt pour demander à l'IA de chunker
prompt_template = """
Split the provided document into logical sections
suitable for a Q&A system.

Each section should be self-contained and cover
a specific topic or concept.

<DOCUMENT>
{document}
</DOCUMENT>

Use this format:

## Section Name

Section content with all relevant details

---

## Another Section Name

Another section content

---
""".strip()


def llm_chunking(text):
    """
    Split text using OpenAI GPT into logical chunks
    """
    prompt = prompt_template.format(document=text)
    
    response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=[{"role": "user", "content": prompt}]
    )
    
    output = response.output_text
    sections = [s.strip() for s in output.split('---') if s.strip()]
    return sections


# Charger tes docs FAQ
with open("faq_docs.json", "r", encoding="utf-8") as f:
    faq_docs = json.load(f)

# Stocker les chunks
faq_chunks_intelligent = []

for doc in tqdm(faq_docs):
    doc_copy = doc.copy()
    content = doc_copy.pop("content", "")
    sections = llm_chunking(content)
    for section in sections:
        chunk = {"chunk": section}
        chunk.update(doc_copy)
        faq_chunks_intelligent.append(chunk)

# Sauvegarder
with open("faq_chunks_intelligent.json", "w", encoding="utf-8") as f:
    json.dump(faq_chunks_intelligent, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(faq_chunks_intelligent)} intelligent chunks")
