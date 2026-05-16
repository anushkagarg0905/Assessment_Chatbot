from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import os

model = None
index = None
assessments = None


def load_resources():

    global model
    global index
    global assessments

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if index is None:
        index = faiss.read_index(
            os.path.join("catalog", "faiss.index")
        )

    if assessments is None:
        with open(
            os.path.join("catalog", "metadata.pkl"),
            "rb"
        ) as f:
            assessments = pickle.load(f)


def retrieve_assessments(query, top_k=5):

    load_resources()

    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(assessments):
            results.append(assessments[idx])

    return results
