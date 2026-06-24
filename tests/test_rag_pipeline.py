import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.parser import parse_document
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.vector_store import store_chunks, search_chunks
from app.services.llm import generate_answer

def run_full_pipeline(filepath: str, content_type: str, query: str):
    print(f"\n{'-'*50}")
    print(f"Pipeline test: {os.path.basename(filepath)}")
    print(f"Query: {query}")
    print(f"{'-'*50}")
    
    # Ingest
    with open(filepath, "rb") as f:
        contents = f.read()
    
    raw = parse_document(contents, content_type)
    cleaned = clean_text(raw)
    chunks = chunk_text(
        text=cleaned,
        doc_id="integration-test-001",
        filename=os.path.basename(filepath),
    )
    embedded = embed_chunks(chunks)
    stored = store_chunks(embedded)
    print(f"Stored: {stored} chunks")

    time.sleep(1)

    # Retrieve
    results = search_chunks(query=query, top_k=3)
    print(f"Retrieved: {len(results)} chunks")
    print(f"Top result score: {results[0]['score']:.4f}")
    print(f"Top result preview: {results[0]['chunk_text'][:120]}")

    # Generate
    answer = generate_answer(query=query, context_chunks=results)
    print(f"\nAnswer: {answer}")

    assert stored > 0, "No chunks stored"
    assert len(results) > 0, "No chunks retrieved"
    assert len(answer) > 0, "Empty answer returned"
    assert "error" not in answer.lower(), "Answer contains error"
    print("\nAll assertions passed.")

run_full_pipeline(
    filepath="tests/fixtures/sample.txt",
    content_type="text/plain",
    query="What is SpaceX's ticker symbol on Nasdaq?"
)
