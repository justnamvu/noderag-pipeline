import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.embedder import embed_chunks
from app.services.vector_store import store_chunks
from app.services.opensearch_client import get_client
from app.core.config import settings


def test_store_chunks():
    print("\n--- Test 1: Store embedded chunks ---")

    mock_chunks = [
        {
           "chunk_index": 0,
           "doc_id": "sample.txt",
           "filename": "sample.txt",
           "chunk_text": "Dave watched as the forest burned up on the hill,",
           "char_count": 49, 
        },
        {
            "chunk_index": 1,
            "doc_id": "sample.txt",
            "filename": "sample.txt",
            "chunk_text": "He picked up the burnt end of the branch and made a mark on the stone.",
            "char_count": 70,
        },
    ]

    embedded = embed_chunks(mock_chunks)
    stored = store_chunks(embedded)

    print(f"Chunks embedded: {len(embedded)}")
    print(f"Chunks stored: {stored}")
    print(f"All stored: {stored == len(mock_chunks)}")


def test_verify_in_opensearch():
    print("\n--- Test 2: Verify chunks exist in OpenSearch ---")

    time.sleep(1)

    client = get_client()
    index_name = settings.opensearch_index_name


    result = client.get(index=index_name, id="sample_0")
    source = result["_source"]

    print(f"doc_id: {source['doc_id']}")
    print(f"filename: {source['filename']}")
    print(f"chunk_index: {source['chunk_index']}")
    print(f"char_count: {source['char_count']}")
    print(f"chunk_text: {source['chunk_text']}")
    print(f"embedding dims: {len(source['embedding'])}")
    print(f"embedding correct: {len(source['embedding']) == 1536}")


def test_count_documents():
    print("\n--- Test 3: Document count in index ---")

    time.sleep(1)
    client = get_client()
    index_name = settings.opensearch_index_name

    response = client.count(index=index_name)
    count = response["count"]
    print(f"Total documents in '{index_name}': {count}")


def test_empty_input():
    print("\n--- Test 4: Empty input ---")
    result = store_chunks([])
    print(f"Result for empty list: {result} (expected 0)")


test_store_chunks()
test_verify_in_opensearch()
test_count_documents()
test_empty_input()