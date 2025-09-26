from minsearch import Index, VectorSearch
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm.auto import tqdm
import json

# Charger les chunks
with open("faq_chunks_paragraphs.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Chunks chargés : {len(chunks)}")

# Index lexical (text search)
faq_tindex = Index(
    text_fields=["chunk"],   # les champs texte à indexer
    keyword_fields=[]        # pas besoin de keywords ici
)
faq_tindex.fit(chunks)

# Modèle d’embeddings (vector search)
embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")

# Génération des embeddings
faq_embeddings = []
for d in tqdm(chunks):
    v = embedding_model.encode(d["chunk"])
    faq_embeddings.append(v)

faq_embeddings = np.array(faq_embeddings)

# Index vectoriel
faq_vindex = VectorSearch(keyword_fields=[])
faq_vindex.fit(faq_embeddings, chunks)

# --- Boucle interactive ---
while True:
    query = input("\n❓ Pose ta question (ou 'exit' pour quitter) : ")
    if query.lower() in ["exit", "quit", "q"]:
        break

    print("\n🔍 Résultats textuels :")
    for r in faq_tindex.search(query, num_results=3):
        print("-", r["chunk"][:200], "...")

    print("\n🧠 Résultats vectoriels :")
    q_emb = embedding_model.encode(query)
    for r in faq_vindex.search(q_emb, num_results=3):
        print("-", r["chunk"][:200], "...")
