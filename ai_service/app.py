from fastapi import FastAPI
from services.rag_engine import index_repo, answer_question

app = FastAPI()

@app.post("/index-repo")
def index_repo_api(data: dict):
    return index_repo(data["projectId"], data["repoUrl"])

@app.post("/query")
def query_api(data: dict):
    return answer_question(data["projectId"], data["question"])