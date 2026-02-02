from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts):
    """
    texts: list[str] -> returns numpy.ndarray shape (n, dim) as float32
    """
    if isinstance(texts, str):
        texts = [texts]
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return np.array(vectors, dtype="float32")

