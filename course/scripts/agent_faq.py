import asyncio
from typing import List, Any
from minsearch import Index
from pydantic_ai import Agent
import json

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

# --- Étape 2 : Créer l’agent avec Pydantic AI ---
system_prompt = """
Tu es un assistant utile pour un cours.
Utilise l’outil de recherche avant de répondre.
Si rien n’est trouvé, dis-le et propose une réponse générale.
"""

agent = Agent(
    name="faq_agent",
    instructions=system_prompt,
    tools=[text_search],
    model="gpt-4o-mini"
)

# --- Étape 3 : Tester l’agent ---
async def main():
    question = "I just discovered the course, can I join now?"
    result = await agent.run(user_prompt=question)

    print("\n🤖 Réponse de l’agent :")
    print(result.output_text)

if __name__ == "__main__":
    asyncio.run(main())
