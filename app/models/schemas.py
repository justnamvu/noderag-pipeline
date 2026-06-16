from pydantic import BaseModel


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
