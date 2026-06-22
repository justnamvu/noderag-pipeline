import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.vector_store import search_chunks

def test_search_basic():
    print("\n--- Test 1: Basic search ---")
    results = search_chunks("What is SpaceX's ticker symbol on Nasdaq", top_k=3)

    print(f"Results returned: {len(results)}")
    for i, r in enumerate(results):
        print(f"\n  Result {i + 1} (score={r['score']:.4f}):")
        print(f"    filename: {r['filename']}")
        print(f"    chunk_index: {r['chunk_index']}")
        print(f"    chunk_text: {r['chunk_text'][:150]}")

def test_search_empty_query():
    print("\n--- Test 2: Empty query ----")
    results = search_chunks("", top_k = 3)
    print(f"Results for empty query: {len(results)} (expected 0)")

def test_search_top_k():
    print("\n--- Test 3: top_k limits result count")
    results = search_chunks("IPO", top_k=2)
    print(f"Requested top_k=2, got {len(results)} results")
    print(f"Within limit: {len(results) <= 2}")

test_search_basic()
test_search_empty_query()
test_search_top_k()
