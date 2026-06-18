import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.embedder import embed_single, embed_chunks

def test_single_embedding():
    print("\n--- Test 1: Single string embedding ---")
    text = "The quarterly revenue increased significantly in Q3."
    vector = embed_single(text)

    print(f"Vector dimensions: {len(vector)} (expected 1536)")
    print(f"Dimensions match: {len(vector) == 1536}")

    all_floats = all(isinstance(v, float) for v in vector)
    print(f"All values floats: {all_floats}")

    in_range = all(-1.0 <= v <= 1.0 for v in vector)
    print(f"All values in [-1, 1]: {in_range}")

    print(f"Fist 5 values: {[round(v, 6) for v in vector[:5]]}")

def test_chunk_embedding():
    print("\n--- Test 2: embed_chunks with mock chunk dicts ---")
    mock_chunks = [
        {
           "chunk_index": 0,
           "doc_id": "sample.txt",
           "filename": "sample.txt",
           "chunk_text": "Dave watched as the forest burned up on the hill.",
           "char_count": 49, 
        },
        {
            "chunk_index": 1,
            "doc_id": "sample.txt",
            "filename": "sample.txt",
            "chunk_text": "Marta was inside trying to round up the last of the pets.",
            "char_count": 57,
        },
    ]
    
    embedded = embed_chunks(mock_chunks)

    print(f"Input chunks: {len(mock_chunks)}")
    print(f"Output chunks: {len(embedded)}")

    for chunk in embedded:
        has_embedding = "embedding" in chunk
        correct_dims = len(chunk["embedding"]) == 1536
        print(f"    chunk {chunk["chunk_index"]}: "
              f"has_embedding={has_embedding}, "
              f"dims={len(chunk["embedding"])}, "
              f"correct={correct_dims}")
    
    original_untouched = "embedding" not in mock_chunks[0]
    print(f"Original chunks untouched: {original_untouched}")

def test_empty_input():
    print("\n--- Test 3: Empty input ---")
    result = embed_chunks([])
    print(f"Result for empty list: {result} (expected [])")

test_single_embedding()
test_chunk_embedding()
test_empty_input()