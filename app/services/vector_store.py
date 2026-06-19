import logging
from typing import List
from fastapi import HTTPException
from app.services.opensearch_client import get_client
from app.core.config import settings

logger = logging.getLogger(__name__)


def store_chunks(chunks: List[dict]) -> int:
    if not chunks:
        return 0

    client = get_client()
    index_name = settings.opensearch_index_name
    stored_count = 0

    logger.info(f"Storing {len(chunks)} chunks into '{index_name}'...")

    for chunk in chunks:
        doc_id = f"{chunk['doc_id']}_{chunk['chunk_index']}"

        body = {
            "embedding": chunk["embedding"],
            "doc_id": chunk["doc_id"],
            "filename": chunk["filename"],
            "chunk_index": chunk["chunk_index"],
            "chunk_text": chunk["chunk_text"],
            "char_count": chunk["char_count"],
        }

        try:
            client.index(
                index=index_name,
                id=doc_id,
                body=body,
            )
            stored_count += 1
            logger.info(f"  Stored chunk {chunk['chunk_text']}  " f"(id={doc_id})")

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store chunk {chunk['chunk_index']} "
                f"(doc_id={chunk['doc_id']}): str{e}",
            )

    logger.info(f"Storage complete. {stored_count}/{len(chunks)} chunks stored.")
    return stored_count
