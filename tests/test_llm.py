import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.llm import generate_answer

mock_chunks = [
    {
        "chunk_index": 0,
        "doc_id": "test-doc-001",
        "filename": "sample.txt",
        "chunk_text": "Professor Jay Ritter has collected data on U.S. IPOs since 1960.",
        "char_count": 64, 
    },
    {
        "chunk_index": 1,
        "doc_id": "test-doc-001",
        "filename": "sample.txt",
        "chunk_text": "CEO Elon Musk even suggested SpaceX's revenue could hit $1 trillion by 2030",
        "char_count": 75,
    },
]

def test_answerable():
    print("\n--- Test 1: Answerable from context ---")
    answer = generate_answer(
        query="When can SpaceX's revenue hit $1 trillion?",
        context_chunks=mock_chunks,
    )
    print(f"Answer: {answer}")
    print(f"Pass: {"enough information" not in answer.lower() and len(answer) > 0}")

def test_partial():
    print("\n--- Test 2: Partially answerable")
    answer = generate_answer(
        query="What is SpaceX and what does it do?",
        context_chunks=mock_chunks,
    )
    print(f"Answer: {answer}")
    fabricated = any(
        word in answer.lower()
        for word in ["Starlink", "AI", "Spacecraft", "Rocket", "NASA"]
    )
    print(f"Pass (no fabricated information): {not fabricated}")

def test_out_of_context():
    print("\n--- Test 3: Out of context")
    answer = generate_answer(
        query="What is the GDP of Vietnam in 2025?",
        context_chunks=mock_chunks,
    )
    print(f"Answer: {answer}")
    print(f"Pass (refuse to hallucinate): {"enough information" in answer.lower()}")

def test_empty_chunks():
    print("\n--- Test 4: Empty chunks ---")
    answer = generate_answer(query="What happened?",context_chunks=[])
    print(f"Answer: {answer}")
    print(f"Pass (faillback triggered): {'enough information' in answer.lower()}")

def test_empty_query():
    print("\n--- Test 5: Empty query ---")
    try:
        generate_answer(query= "   ", context_chunks=mock_chunks)
        print("Fail (should have raised HTTPException)")
    except Exception as e:
        print(f"Correctly raised: {e}")
        print("Pass")

test_answerable()
test_partial()
test_out_of_context()
test_empty_chunks()
test_empty_query()
