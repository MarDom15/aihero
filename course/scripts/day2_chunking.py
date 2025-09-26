import json
import re

# --- 1. Fonction sliding window ---
def sliding_window(seq, size, step):
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")

    n = len(seq)
    result = []
    for i in range(0, n, step):
        chunk = seq[i:i+size]
        result.append({'start': i, 'chunk': chunk})
        if i + size >= n:
            break
    return result


# --- 2. Fonction paragraph splitting ---
def split_by_paragraphs(text):
    """
    Coupe un texte en paragraphes (séparés par une ligne vide).
    """
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


# --- 3. Fonction section splitting (Markdown headers) ---
def split_markdown_by_level(text, level=2):
    """
    Coupe un texte markdown par niveau de titre (#, ##, ###).
    """
    header_pattern = r'^(#{' + str(level) + r'} )(.+)$'
    pattern = re.compile(header_pattern, re.MULTILINE)

    parts = pattern.split(text)
    sections = []

    for i in range(1, len(parts), 3):
        header = parts[i] + parts[i+1]  # ex: "## " + "Titre"
        header = header.strip()

        content = ""
        if i+2 < len(parts):
            content = parts[i+2].strip()

        if content:
            section = f"{header}\n\n{content}"
        else:
            section = header
        sections.append(section)

    return sections


# --- 4. Charger les docs sauvegardés hier ---
with open("faq_docs.json", "r", encoding="utf-8") as f:
    faq_docs = json.load(f)

print(f"Documents chargés : {len(faq_docs)}")


# --- 5. Appliquer les 3 méthodes de chunking ---

## (a) Sliding window
faq_chunks_sliding = []
for doc in faq_docs:
    doc_copy = doc.copy()
    content = doc_copy.pop("content", "")
    chunks = sliding_window(content, size=2000, step=1000)
    for chunk in chunks:
        chunk.update(doc_copy)
    faq_chunks_sliding.extend(chunks)

print(f"Chunks sliding window : {len(faq_chunks_sliding)}")


## (b) Paragraph splitting
faq_chunks_paragraphs = []
for doc in faq_docs:
    doc_copy = doc.copy()
    content = doc_copy.pop("content", "")
    paragraphs = split_by_paragraphs(content)
    for para in paragraphs:
        chunk = {"chunk": para}
        chunk.update(doc_copy)
        faq_chunks_paragraphs.append(chunk)

print(f"Chunks paragraphes : {len(faq_chunks_paragraphs)}")


## (c) Section splitting (niveau 2)
faq_chunks_sections = []
for doc in faq_docs:
    doc_copy = doc.copy()
    content = doc_copy.pop("content", "")
    sections = split_markdown_by_level(content, level=2)
    for section in sections:
        chunk = {"chunk": section}
        chunk.update(doc_copy)
        faq_chunks_sections.append(chunk)

print(f"Chunks sections (##) : {len(faq_chunks_sections)}")


# --- 6. Sauvegarde des résultats ---
with open("faq_chunks_sliding.json", "w", encoding="utf-8") as f:
    json.dump(faq_chunks_sliding, f, ensure_ascii=False, indent=2)

with open("faq_chunks_paragraphs.json", "w", encoding="utf-8") as f:
    json.dump(faq_chunks_paragraphs, f, ensure_ascii=False, indent=2)

with open("faq_chunks_sections.json", "w", encoding="utf-8") as f:
    json.dump(faq_chunks_sections, f, ensure_ascii=False, indent=2)

print("✅ Sauvegardé les 3 fichiers de chunks (sliding, paragraphes, sections)")
