import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.models.schemas import UploadResponse
from app.services.parser import parse_document
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text

router = APIRouter()

ALLOWED_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. "
            "Allowed: pdf, txt, docx",
        )

    contents = await file.read()
    file_size = len(contents)
    max_bytes = settings.max_file_size_mb * 1024 * 1024

    if file_size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size} bytes. Max allowed: {max_bytes} bytes",
        )

    doc_id = str(uuid.uuid4())
    raw_text = parse_document(contents, file.content_type)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(
        text=cleaned_text,
        doc_id=doc_id,
        filename=file.filename,
    )

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        content_type=file.content_type,
        file_size_bytes=file_size,
        char_count=len(cleaned_text),
        chunk_count=len(chunks),
        message=f"Pipeline complete. {len(chunks)} chunks ready for embedding.",
    )
