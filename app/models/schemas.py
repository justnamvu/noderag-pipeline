from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):  # what a successful upload returns
    doc_id: str
    filename: str
    content_type: str
    file_size_bytes: int
    char_count: int
    chunk_count: int
    message: str


class ErrorResponse(BaseModel):  # what FastAPI returns on 400 or 422
    detail: str


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class ChunkResult(BaseModel):
    doc_id: str
    filename: str
    chunk_index: int
    chunk_text: str
    char_count: int
    score: float


class QueryResponse(BaseModel):
    query: str
    results: List[ChunkResult]
    result_count: int
