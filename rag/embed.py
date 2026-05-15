import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load assessments
with open("catalog/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

print(f"Loaded {len(assessments)} assessments")

# Load MiniLM model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []

# Prepare text
for item in assessments:

    combined_text = f"""
    Name: {item['name']}
    Description: {item['description']}
    """

    texts.append(combined_text)

# Create embeddings
embeddings = model.encode(texts)

print("Embeddings created")

# Convert embeddings
embedding_matrix = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embedding_matrix.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embedding_matrix)

print("FAISS index created")

# Save index
faiss.write_index(index, "catalog/faiss.index")

# Save metadata
with open("catalog/metadata.pkl", "wb") as f:
    pickle.dump(assessments, f)

print("Saved FAISS index and metadata")