import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.cleaner import clean_text
from app.services.parser import parse_document

def test_cleaner_on_string():
    print("\n--- Test 1: Direct string cleaning ---")
    dirty = "This   has\t\ttabs  and   spaces.\n\n\n\nToo many newlines.\xa0Non-breaking space.\xadSoft hyphen.\u2022 Bullet point."
    cleaned = clean_text(dirty)
    print(f"Before: {repr(dirty)}")
    print(f"After: {repr(cleaned)}")

def test_cleaner_on_fixture(path: str, content_type: str):
    print(f"\n--- Test 2: Clean parsed fixture: {path} ---")
    with open(path, "rb") as f:
        contents = f.read()
    raw = parse_document(contents, content_type)
    cleaned = clean_text(raw)
    print(f"Raw length: {len(raw)} chars")
    print(f"Cleaned length: {len(cleaned)} chars")
    print(f"Chars removed: {len(raw) - len(cleaned)}")
    print(f"First 200 chars of cleaned text:\n{cleaned[:200]}")

test_cleaner_on_string()
test_cleaner_on_fixture("tests/fixtures/sample.txt",  "text/plain")
test_cleaner_on_fixture("tests/fixtures/sample.pdf",  "application/pdf")
test_cleaner_on_fixture("tests/fixtures/sample.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
