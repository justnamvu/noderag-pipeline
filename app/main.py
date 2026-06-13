from fastapi import FastAPI
from app.api.routes import upload

app = FastAPI(title="NodeRAG", version="0.1.0")

app.include_router(upload.router, prefix="/api/v1", tags=["ingestion"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
