import faiss
import os
import pickle

VECTOR_SIZE = 384
BASE_PATH = "./storage/indexes"

def save_index(project_id, vectors, metadata):
    
    index = faiss.IndexFlatL2(VECTOR_SIZE)
    index.add(vectors)

    os.makedirs(BASE_PATH, exist_ok=True)

    faiss.write_index(index, f"{BASE_PATH}/{project_id}.index")

    with open(f"{BASE_PATH}/{project_id}.meta", "wb") as f:
        pickle.dump(metadata, f)


def load_index(project_id):
    index = faiss.read_index(f"{BASE_PATH}/{project_id}.index")

    with open(f"{BASE_PATH}/{project_id}.meta", "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
