import requests
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000/documents/"

# Elasticsearch client for cleanup
elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
es = Elasticsearch(elastic_url, api_key=elastic_api_key)

def test_upload_pdfs():
    files = [
        ("files", open("tests/samples/LB5001.pdf", "rb")),
        ("files", open("tests/samples/MN414_0224.pdf", "rb")),
    ]

    index_name = "test_index_123"
    data = {
        "user_id": "test_user",
        "session_id": "test_session",
        "index_name": index_name
    }

    response = requests.post(API_URL, files=files, data=data)
    result = response.json()
    print("Response:", result)

    assert response.status_code == 200
    assert "documents_indexed" in result
    assert "total_chunks" in result
    assert result["documents_indexed"] == 2

    # Cleanup: delete index
    try:
        es.indices.delete(index=index_name)
        print(f"Deleted test index '{index_name}' successfully.")
    except Exception as e:
        print(f"Failed to delete test index '{index_name}': {e}")

if __name__ == "__main__":
    test_upload_pdfs()
    print("API /documents test passed!")
