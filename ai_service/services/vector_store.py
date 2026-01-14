import faiss
import os
import pickle
import numpy as np

VECTOR_SIZE = 384
BASE_PATH = "./storage/indexes"

def save_index(project_id: str, vectors: np.ndarray, metadata: list):
    """
    Save FAISS index and metadata for project_id.
    vectors: numpy array shape (n, dim), dtype float32
    metadata: list of dicts (one per vector)
    """
    os.makedirs(BASE_PATH, exist_ok=True)

    n, dim = vectors.shape
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, os.path.join(BASE_PATH, f"{project_id}.index"))

    with open(os.path.join(BASE_PATH, f"{project_id}.meta"), "wb") as f:
        pickle.dump(metadata, f)

def load_index(project_id: str):
    idx_path = os.path.join(BASE_PATH, f"{project_id}.index")
    meta_path = os.path.join(BASE_PATH, f"{project_id}.meta")

    if not os.path.exists(idx_path) or not os.path.exists(meta_path):
        raise FileNotFoundError("Index or metadata not found for project_id: " + project_id)

    index = faiss.read_index(idx_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata