import os
import uuid
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from app.pipeline.index import ElasticVectorManager
from app.pipeline.extract import PdfReader

load_dotenv()

API_URL = "http://127.0.0.1:8000/"
ENDPOINT = f"{API_URL}question/"

pdf_path = "tests/samples/LB5001.pdf"

# Elasticsearch client for cleanup
elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
es = Elasticsearch(elastic_url, api_key=elastic_api_key)

def test_generate_answer():
    index_name = "test_index_qa_123"

    # generate some dummy data
    reader = PdfReader(user_id="test_user", session_id="test_session")
    index_name = f"test-index-{uuid.uuid4().hex[:8]}"
    vector_database = ElasticVectorManager(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=index_name,
    )

    docs = reader.read(pdf_path)
    vector_database.index_documents(docs)

    payload = {
        "user_id": "test_user",
        "session_id": "test_session",
        "index_name": index_name,
        "question": "What is in the test documents?"
    }

    response = requests.post(ENDPOINT, json=payload)
    result = response.json()
    print("Response:", result)

    assert response.status_code == 200
    assert "response" in result, "Response missing expected answer field"

    # Cleanup: delete index
    try:
        es.indices.delete(index=index_name)
        print(f"Deleted test index '{index_name}' successfully.")
    except Exception as e:
        print(f"Failed to delete test index '{index_name}': {e}")

if __name__ == "__main__":
    test_generate_answer()
    print("API /questions test passed!")
