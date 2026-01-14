from services.llm_client import generate
from services.rag_engine import index_repo, answer_question

# print(generate("Explain RAG in simple words"))


res = index_repo("demo_proj", "https://github.com/ayushks404/contextual_codebase_backend")  # or small repo
print(res)

# test query (after indexing finishes)
out = answer_question("demo_proj", "What does this repo do?")
print(out)