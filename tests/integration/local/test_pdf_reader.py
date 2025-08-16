import os
from app.pipeline.extract import PdfReader

pdf_path = "tests/samples/LB5001.pdf"

def test_reader_local_pdf():
    """Testing the reader with a local PDF file"""
    reader = PdfReader()
    docs = reader.read(pdf_path)

    assert isinstance(docs, list), "Reader should return a list of docs"
    assert len(docs) > 0, "PDF should have at least one document chunk"

    print("PDF reader test passed!")
    print(f"Extracted {len(docs)} document chunks.")

if __name__ == "__main__":
    test_reader_local_pdf()
