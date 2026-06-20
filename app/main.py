from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import upload, query
from app.services.index_manager import create_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_index()
    yield


app = FastAPI(title="NodeRAG", version="0.1.0", lifespan=lifespan)

app.include_router(upload.router, prefix="/api/v1", tags=["ingestion"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
