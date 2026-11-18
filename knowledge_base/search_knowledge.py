import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

# Locate vector storage
BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index(str(VECTOR_DIR / "knowledge.index"))

# Load knowledge chunks
with open(VECTOR_DIR / "chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)


def search_knowledge(query, top_k=3):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "similarity": float(score)
        })

    return results


if __name__ == "__main__":
    question = input("Enter your travel question: ")

    results = search_knowledge(question)

    for result in results:
        print("\nSource:", result["source"])
        print("Similarity:", round(result["similarity"], 3))
        print("Information:", result["text"])