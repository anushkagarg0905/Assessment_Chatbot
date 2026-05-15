from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np


# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index
index = faiss.read_index("catalog/faiss.index")

# metadata
with open("catalog/metadata.pkl", "rb") as f:
    assessments = pickle.load(f)


def retrieve_assessments(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode([query])

    # Convert to float32
    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    # Collect matching assessments
    for idx in indices[0]:

        if idx < len(assessments):

            results.append(assessments[idx])

    return results


# Test retrieval directly
if __name__ == "__main__":

    query = "Java developer with leadership skills"

    results = retrieve_assessments(query)

    print("\nTop Results:\n")

    for i, item in enumerate(results, 1):

        print(f"{i}. {item['name']}")
        print(item["url"])
        print()