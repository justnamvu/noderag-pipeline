from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    content_type: str
    file_size_bytes: int
    char_count: int
    chunk_count: int
    message: str


class ErrorResponse(BaseModel):
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
    answer: str
    sources: List[ChunkResult]
    source_count: int
