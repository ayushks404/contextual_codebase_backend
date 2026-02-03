FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')"
COPY . .


CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
