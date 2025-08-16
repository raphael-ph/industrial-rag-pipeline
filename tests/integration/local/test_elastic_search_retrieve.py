import os
import uuid
from dotenv import load_dotenv
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager
from app.pipeline.retrieve import ElasticRetriever
from app.utils.logger import Logger

load_dotenv()
_log = Logger.get_logger(__name__)

elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
pdf_path = "tests/samples/LB5001.pdf"

def test_retrieval():
    """Test Elasticsearch retrieval."""
    # Temporary index
    index_name = f"test-index-{uuid.uuid4().hex[:8]}"
    vector_database = ElasticVectorManager(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=index_name,
    )

    reader = PdfReader()
    docs = reader.read(pdf_path)
    vector_database.index_documents(docs)

    retriever = ElasticRetriever(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=index_name,
    )

    query = "What is the process before accepting a motor?"
    results = retriever.retrieve(query)
    print(results)
    assert len(results) > 0, "Retriever returned no documents"
    assert "motor" in results[0]["text"].lower(), "First retrieved doc does not mention 'motor'"

    print("Retrieval test passed!")
    print(f"Retrieved {len(results)} documents.")

    # Cleanup
    try:
        vector_database.es.indices.delete(index=index_name)
        _log.info(f"Deleted temporary index {index_name}")
    except Exception as e:
        _log.warning(f"Failed to delete temporary index {index_name}: {e}")


if __name__ == "__main__":
    test_retrieval()
