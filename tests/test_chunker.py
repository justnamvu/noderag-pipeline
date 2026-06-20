import sys 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.parser import parse_document
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text

def test_chunker(path: str, content_type: str):
    print(f"\n{'-'*50}")
    print(f"Testing full pipeline: {path}")
    print(f"{'-'*50}")

    with open(path, "rb") as f:
        contents = f.read()
    
    raw_text = parse_document(contents, content_type)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(
        text=cleaned_text,
        doc_id="test-doc-id",
        filename=os.path.basename(path),
        chunk_size=500,
        overlap=50,
    )

    print(f"\nFirst chunk preview:")
    print(f"index: {chunks[0]['chunk_index']}")
    print(f"doc_id: {chunks[0]['doc_id']}")
    print(f"filename: {chunks[0]['filename']}")
    print(f"char_count: {chunks[0]['char_count']}")
    print(f"text: {chunks[0]['chunk_text'][:200]}")

    if len(chunks) > 1:
        print(f"\nOverlap check (last 50 chars of chunk 0 vs first 50 chars of chunk 1):")
        print(f"End of chunk 0: ...{chunks[0]['chunk_text'][-50:]!r}")
        print(f"Start of chunk 1: {chunks[1]['chunk_text'][:50]!r}...")

def test_edge_cases():
    print(f"\n{'-'*50}")
    print("Testing edge cases")
    print(f"{'-'*50}")

    print("\n--- Empty string ---")
    result = chunk_text("", doc_id="x", filename="empty.txt")
    print(f"Chunks from emtpy string: {len(result)} (expected 0)")

    print("\n--- Short string (less than chunk_size) ---")
    result = chunk_text("Short text.", doc_id="x", filename="short.txt")
    print(f"Chunks from short string: {len(result)} (expected 1)")
    print(f"Content: {result[0]['text']!r}")

    print("\n--- Whitespace-only stirng ---")
    result = chunk_text("     \n\n     ", doc_id="x", filename="blank.txt")
    print(f"Chunks from whitespace string: {len(result)} (expected 0)")

test_edge_cases()
test_chunker("tests/fixtures/sample.txt", "text/plain")
test_chunker("tests/fixtures/sample.pdf", "application/pdf")
test_chunker("tests/fixtures/sample.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
