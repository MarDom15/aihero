import json
import random

def show_examples(file, n=3):
    print(f"\n=== Exemple depuis {file} ===")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Nombre total de chunks : {len(data)}")

    # choisir n chunks au hasard
    examples = random.sample(data, min(n, len(data)))
    for i, ex in enumerate(examples, 1):
        print(f"\n--- Chunk {i} ---")
        # affiche le titre s'il existe
        if "title" in ex:
            print(f"Titre : {ex['title']}")
        if "filename" in ex:
            print(f"Fichier : {ex['filename']}")
        print("Contenu :")
        print(ex.get("chunk", "")[:500])  # max 500 caractères pour éviter trop long


if __name__ == "__main__":
    # 3 fichiers générés hier
    files = [
        "faq_chunks_sliding.json",
        "faq_chunks_paragraphs.json",
        "faq_chunks_sections.json"
    ]

    for file in files:
        show_examples(file, n=3)
