from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.vector_store import search_chunks

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    results = search_chunks(query=request.query, top_k=request.top_k)

    return QueryResponse(
        query=request.query,
        results=results,
        result_count=len(results),
    )
