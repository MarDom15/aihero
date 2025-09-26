import json
from tqdm.auto import tqdm
import numpy as np
from sentence_transformers import SentenceTransformer
from minsearch import Index, VectorSearch

# === Charger les données ===
with open("faq_chunks_paragraphs.json", "r", encoding="utf-8") as f:
    faq_chunks = json.load(f)

print(f"Chunks chargés : {len(faq_chunks)}")

# === 1. Index lexical (text search) ===
faq_index = Index(
    text_fields=["chunk"],   # on cherche dans le texte des chunks
    keyword_fields=[]        # pas de champs mots-clés exacts
)
faq_index.fit(faq_chunks)

# === 2. Index vectoriel (vector search) ===
embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")

faq_embeddings = []
for d in tqdm(faq_chunks):
    text = d["chunk"]
    v = embedding_model.encode(text)
    faq_embeddings.append(v)

faq_embeddings = np.array(faq_embeddings)

faq_vindex = VectorSearch(keyword_fields=[])
faq_vindex.fit(faq_embeddings, faq_chunks)

# === 3. Fonctions de recherche ===
def text_search(query, k=5):
    return faq_index.search(query, num_results=k)

def vector_search(query, k=5):
    q = embedding_model.encode(query)
    return faq_vindex.search(q, num_results=k)

def hybrid_search(query, k=5):
    text_results = text_search(query, k)
    vector_results = vector_search(query, k)

    # Combine & supprime doublons
    seen_ids = set()
    combined = []
    for r in text_results + vector_results:
        rid = r.get("id", r.get("filename", None))
        if rid not in seen_ids:
            seen_ids.add(rid)
            combined.append(r)
    return combined

# === 4. Test ===
query = "What should be in a test dataset for AI evaluation?"

print("\n🔍 Résultats textuels :")
for r in text_search(query):
    print("-", r["chunk"][:200], "...")

print("\n🧠 Résultats vectoriels :")
for r in vector_search(query):
    print("-", r["chunk"][:200], "...")

print("\n🔄 Résultats hybrides :")
for r in hybrid_search(query):
    print("-", r["chunk"][:200], "...")
