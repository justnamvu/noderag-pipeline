import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.vector_store import search_chunks

def test_search_basic():
    print("\n--- Test 1: Basic search ---")
    results = search_chunks("What is SpaceX's ticker symbol on Nasdaq?", top_k=3)

    print(f"Number of results: {len(results)}")
    for i, result in enumerate(results):
        print(f"\nResult {i + 1} (score={result['score']:.4f}):")
        print(f"    filename: {result['filename']}")
        print(f"    chunk_index: {result['chunk_index']}")
        print(f"    chunk_text: {result['chunk_text'][:150]}")

def test_search_empty():
    print("\n--- Test 2: Search empty query ----")
    results = search_chunks("", top_k=3)
    print(f"Results for empty query: {len(results)} (expected 0)")

def test_check_top_k():
    print("\n--- Test 3: Check top_k limits")
    results = search_chunks("IPO", top_k=2)
    print(f"Requested top_k=2, got {len(results)} results")
    print(f"Within limit: {len(results) <= 2}")

test_search_basic()
test_search_empty()
test_check_top_k()
