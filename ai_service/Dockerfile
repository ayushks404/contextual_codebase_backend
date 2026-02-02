FROM python:3.11

WORKDIR /app

COPY ai_service/requirements.txt .
RUN pip install -r requirements.txt

COPY ai_service/ ./

EXPOSE 10000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
