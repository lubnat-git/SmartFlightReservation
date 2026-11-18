
import json
import re
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"
VECTOR_DIR.mkdir(exist_ok=True)

DOCUMENTS = [
    BASE_DIR / "travel_faq.txt",
    BASE_DIR / "travel_policies.txt",
]

MODEL_NAME = "all-MiniLM-L6-v2"


def is_heading_only(paragraph):
    lines = [
        line.strip()
        for line in paragraph.splitlines()
        if line.strip()
    ]

    if not lines:
        return True

    meaningful_lines = []

    for line in lines:
        # Ignore decorative separator lines
        if re.fullmatch(r"[=\-_*#\s]+", line):
            continue

        # Ignore document version metadata
        if re.fullmatch(
            r"Version:\s*\d+(?:\.\d+)*",
            line,
            re.IGNORECASE
        ):
            continue

        meaningful_lines.append(line)

    if not meaningful_lines:
        return True

    # Exclude paragraphs containing only uppercase headings
    return all(
        line == line.upper()
        for line in meaningful_lines
        if any(char.isalpha() for char in line)
    )


model = SentenceTransformer(MODEL_NAME)

chunks = []

for document in DOCUMENTS:
    text = document.read_text(encoding="utf-8")

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    for paragraph in paragraphs:
        if len(paragraph) <= 30:
            continue

        if is_heading_only(paragraph):
            continue

        chunks.append({
            "text": paragraph,
            "source": document.name
        })


if not chunks:
    raise ValueError("No knowledge-base content found.")


texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(
    index,
    str(VECTOR_DIR / "knowledge.index")
)

with open(
    VECTOR_DIR / "chunks.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        chunks,
        file,
        indent=4,
        ensure_ascii=False
    )


print(f"Successfully generated {len(chunks)} embeddings.")
print(f"Vector index contains {index.ntotal} vectors.")
print(f"Vector index saved to: {VECTOR_DIR}")
