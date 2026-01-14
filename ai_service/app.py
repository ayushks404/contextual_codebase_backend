from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.rag_engine import index_repo, answer_question

app = FastAPI(title="CCA AI Service")

#Models

class IndexRequest(BaseModel):
    project_id: str
    repo_url: str

class QueryRequest(BaseModel):
    project_id: str
    question: str

#Routes

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/index-repo")
def index_repository(req: IndexRequest):
    try:
        result = index_repo(req.project_id, req.repo_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_repository(req: QueryRequest):
    try:
        result = answer_question(req.project_id, req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
