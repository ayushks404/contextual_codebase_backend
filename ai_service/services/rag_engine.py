from services.repo_cloner import clone_repo
from services.chunker import read_files, chunk_code
from services.embeddings import generate_embeddings
from services.vector_store import save_index, load_index
from services.llm_client import generate


def index_repo(project_id, repo_url):
    repo_path = clone_repo(repo_url, project_id)

    files = read_files(repo_path)

    chunks = []
    metadata = []

    for file in files:
        parts = chunk_code(file)
        for part in parts:
            chunks.append(part)
            metadata.append({"file": file})

    vectors = generate_embeddings(chunks)

    save_index(project_id, vectors, metadata)

    return {"status": "indexed", "files": len(files), "chunks": len(chunks)}


def answer_question(project_id, question):
    index, metadata = load_index(project_id)

    query_vector = generate_embeddings([question])

    D, I = index.search(query_vector, k=5)

    context = ""
    sources = []

    for i in I[0]:
        context += metadata[i]["file"] + "\n"
        sources.append(metadata[i])

    prompt = f"""
You are a senior software engineer.

Use the following code context to answer the question.

Context:
{context}

Question:
{question}
"""

    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": sources
    }
