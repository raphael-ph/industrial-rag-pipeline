from app.pipeline.extract import PdfReader

pdf_path = "tests/samples/LB5001.pdf"

def test_reader_local_pdf():
    """Testing the reader with a local PDF file"""
    reader = PdfReader()
    docs = reader.read(pdf_path)

    print(docs)

if __name__ == "__main__":
    print("Begining first test: test_reader_local_pdf()")
    print(f"{80*'='} load_test_reader_local_pdf() {80*'='}")
    test_reader_local_pdf()