import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.parser import parse_document
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text

def print_chunks(filepath, content_type):
    print(f"\n{'-'*50}")
    print(f"Chunks for: {os.path.basename(filepath)}")
    print(f"{'-'*50}")
    with open(filepath, "rb") as f:
        contents = f.read()
    raw = parse_document(contents, content_type)
    cleaned = clean_text(raw)
    chunks = chunk_text(
        text=cleaned,
        doc_id="preview",
        filename=os.path.basename(filepath),
    )
    for chunk in chunks:
        print(
            f"\n[chunk_index={chunk['chunk_index']}] "
            f"({chunk['char_count']} chars)"
        )
        print(chunk['chunk_text'])

print_chunks("backend/tests/fixtures/sample.txt", "text/plain")