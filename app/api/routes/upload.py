import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.models.schemas import UploadResponse

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
            detail=f"Unsupported file type: {file.content_type}. Allowed: pdf, txt, docx",
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

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        content_type=file.content_type,
        file_size_bytes=file_size,
        message="File received successfully. Parsing will follow.",
    )
