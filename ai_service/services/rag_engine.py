# services/rag_engine.py
from services.repo_cloner import clone_repo
from services.chunker import read_files, chunk_code
from services.embeddings import generate_embeddings
from services.vector_store import save_index, load_index
from services.llm_client import generate

import os

def index_repo(project_id: str, repo_url: str):
    repo_path = clone_repo(repo_url, project_id)

    files = read_files(repo_path)

    chunks = []
    metadata = []

    for file in files:
        parts = chunk_code(file)
        for part in parts:
            chunks.append(part)
            metadata.append({"file": file})

    if not chunks:
        return {"status": "no_chunks", "files": len(files), "chunks": 0}

    vectors = generate_embeddings(chunks)  # numpy float32

    save_index(project_id, vectors, metadata)

    return {"status": "indexed", "files": len(files), "chunks": len(chunks)}

def answer_question(project_id: str, question: str, k: int = 5):
    index, metadata = load_index(project_id)

    query_vector = generate_embeddings([question])

    D, I = index.search(query_vector, k)

    # I is shape (1, k)
    retrieved_chunks = []
    sources = []
    for idx in I[0]:
        if idx < 0 or idx >= len(metadata):
            continue
        retrieved_chunks.append(metadata[idx].get("file", "") + "\n")
        sources.append(metadata[idx])

    context = "\n".join(retrieved_chunks)

    prompt = f"""You are a senior software engineer.

Use the following code context to answer the question (cite file paths).

Context:
{context}

Question:
{question}
"""

    answer = generate(prompt)

    return {"answer": answer, "sources": sources}
