import asyncio
from typing import List, Any
from minsearch import Index
import json
from datetime import datetime

# --- Étape 1 : Charger les chunks et préparer la fonction de recherche ---
with open("faq_chunks_paragraphs.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

faq_tindex = Index(
    text_fields=["chunk"],
    keyword_fields=[]
)
faq_tindex.fit(chunks)

def text_search(query: str) -> List[Any]:
    """
    Cherche dans la FAQ indexée avec une recherche textuelle.

    Args:
        query (str): La question ou les mots-clés.
    Returns:
        List[Any]: Les résultats (max 5).
    """
    return faq_tindex.search(query, num_results=5)

# --- Étape 2 : Fonction pour afficher les extraits et expansion ---
def display_results(results: List[Any]):
    print("\nI searched the FAQ and found these relevant excerpts:")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['chunk'][:200]}... [source: {r['source']}]")  # affiche 200 caractères
    print("\nIf you want more details, type 'expand <number>' (e.g., expand 1).")
    print("Or type a new question, or 'exit' to quit.")

def expand_result(results: List[Any], number: int):
    if 1 <= number <= len(results):
        r = results[number - 1]
        print(f"\nExpanded excerpt {number}:")
        print(r['chunk'])
        print(f"[source: {r['source']}]")
    else:
        print("Invalid number. Choose a valid excerpt to expand.")

# --- Étape 3 : Agent offline interactif ---
async def offline_agent():
    print(f"Chunks loaded: {len(chunks)}")
    print("Offline FAQ Agent (no API). Type 'exit' to quit.\n")

    while True:
        question = input("📝 Question: ").strip()
        if question.lower() == "exit":
            print("Bye!")
            break

        results = text_search(question)
        display_results(results)

        # Boucle pour expansion ou nouvelle question
        while True:
            cmd = input("\nCommand (or new question): ").strip()
            if cmd.lower() == "exit":
                print("Bye!")
                return
            elif cmd.lower().startswith("expand"):
                try:
                    num = int(cmd.split()[1])
                    expand_result(results, num)
                except (IndexError, ValueError):
                    print("Use 'expand <number>', e.g., expand 2")
            else:
                # Nouvelle question
                question = cmd
                break

# --- Étape 4 : Lancer l'agent ---
if __name__ == "__main__":
    asyncio.run(offline_agent())
what