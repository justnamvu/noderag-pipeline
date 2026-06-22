import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.llm import generate_answer

MOCK_CHUNKS = [
    {
        "chunk_index": 0,
        "filename": "sample.txt",
        "chunk_text": "Professor Jay Ritter has collected data on U.S. IPOs since 1960.",
    },
    {
        "chunk_index": 1,
        "filename": "sample.txt",
        "chunk_text": "CEO Elon Musk even suggested SpaceX's revenue could hit $1 trillion by 2030",
    },
]

def test_answer_with_context():
    print("\n--- Test 1: Question answerable from context ---")
    answer = generate_answer(
        query="When can SpaceX's revenue hit $1 trillion?",
        context_chunks=MOCK_CHUNKS,
    )
    print(f"Answer: {answer}")
    print(f"\nNon-empty: {len(answer) > 0}")
    print(f"Not 'I don't know': {'enough information' not in answer.lower()}")

def test_answer_out_of_context():
    print("\n--- Test 2: Question not answerable from context")
    answer = generate_answer(
        query="What is the GDP of Vietnam in 2025?",
        context_chunks=MOCK_CHUNKS
    )
    print(f"Answer: {answer}")
    print(f"\nReturned 'I don't know': {'enough information' in answer.lower()}")

def test_empty_chunks():
    print("\n--- Test 3: No chunks provided ---")
    answer = generate_answer(
        query="What happened?",
        context_chunks=[],
    )
    print(f"Answer: {answer}")
    print(f"Returned fallback: {'enough information' in answer.lower()}")

test_answer_with_context()
test_answer_out_of_context()
test_empty_chunks()