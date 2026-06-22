import logging
from typing import List

from openai import OpenAI
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)

_llm_client: OpenAI = None


def get_llm_client() -> OpenAI:
    global _llm_client
    if _llm_client is None:
        _llm_client = OpenAI(api_key=settings.llm_api_key)
    return _llm_client


SYSTEM_PROMPT = """You are a precise document assistant. Your job is to answer
questions strictly based on the context passages provided below.

Rules you must follow:
1. Answer only using information found in the provided context.
2. If the context does not contain enough information to answer the question,
   respond with exactly: "I don't have enough information in the provided
   documents to answer this question."
3. Never fabricate facts, statistics, names, or dates not present in the context.
4. Keep your answer concise and direct.
5. If relevant, mention which part of the context your answer comes from."""


def _build_context_block(chunks: List[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(
            f"[{i}] (file: {chunk['filename']}), "
            f"chunk {chunk['chunk_index']}):\n{chunk['chunk_text']}"
        )
    return "\n\n".join(lines)


def generate_answer(query: str, context_chunks: List[dict]) -> str:
    if not context_chunks:
        return (
            "I don't have enough information in the provided "
            "documents to answer this question."
        )

    client = get_llm_client()
    context_block = _build_context_block(context_chunks)

    user_message = f"""Context passages:

        {context_block}

        Question: {query}

        Answer based strictly on the context above."""

    logger.info(
        f"Generating answer for query: '{query[:60]}...' "
        f"using {len(context_chunks)} context chunks"
    )

    try:
        response = client.chat.completions.create(
            model=settings.llm_model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
            max_completion_tokens=500,
        )
        answer = response.choices[0].message.content.strip()
        logger.info("Answer generated successfully.")
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")
