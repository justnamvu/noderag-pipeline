import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.parser import parse_document

def test_file(path: str, content_type: str):
    print(f"\n--- Test: Parse {path} ---")
    with open(path, "rb") as f:
        contents = f.read()
    try:
        text = parse_document(contents, content_type)
        print(f"Status: Ok")
        print(f"Characters extracted: {len(text)}")
        print(f"First 200 chars: {text[:200]}")
    except Exception as e:
        print(f"Status: Failed — {e}")

test_file("backend/tests/fixtures/sample.txt", "text/plain")
test_file("backend/tests/fixtures/sample.pdf", "application/pdf")
test_file("backend/tests/fixtures/sample.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
