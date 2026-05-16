from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import os


# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------

model = None
index = None
assessments = None


# ---------------------------------------------------
# LOAD RESOURCES LAZILY
# ---------------------------------------------------

def load_resources():

    global model
    global index
    global assessments

    if model is None:

        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if index is None:

        print("Loading FAISS index...")
        index = faiss.read_index(
            os.path.join("catalog", "faiss.index")
        )

    if assessments is None:

        print("Loading metadata...")

        with open(
            os.path.join("catalog", "metadata.pkl"),
            "rb"
        ) as f:

            assessments = pickle.load(f)


# ---------------------------------------------------
# RETRIEVAL FUNCTION
# ---------------------------------------------------

def retrieve_assessments(query, top_k=5):

    # Load only when needed
    load_resources()

    # Create embedding
    query_embedding = model.encode([query])

    # Convert datatype
    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    # Collect results
    for idx in indices[0]:

        if idx < len(assessments):

            results.append(
                assessments[idx]
            )

    return results


# ---------------------------------------------------
# LOCAL TEST
# ---------------------------------------------------

if __name__ == "__main__":

    query = "Java developer with leadership skills"

    results = retrieve_assessments(query)

    print("\nTop Results:\n")

    for i, item in enumerate(results, 1):

        print(f"{i}. {item['name']}")
        print(item["url"])
        print()
