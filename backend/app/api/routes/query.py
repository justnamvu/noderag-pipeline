from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.vector_store import search_chunks
from app.services.llm import generate_answer

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    chunks = search_chunks(query=request.query, top_k=request.top_k)

    answer = generate_answer(query=request.query, context_chunks=chunks)

    return QueryResponse(
        query=request.query,
        answer=answer,
        sources=chunks,
        source_count=len(chunks),
    )
