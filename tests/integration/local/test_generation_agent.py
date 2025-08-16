import os
import uuid
from dotenv import load_dotenv
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager
from app.pipeline.retrieve import ElasticRetriever
from app.pipeline.generate import RAGAgent
from app.utils.logger import Logger

load_dotenv()
_log = Logger.get_logger(__name__)

elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
pdf_path = "tests/samples/LB5001.pdf"

def test_generation():
    """Test RAG agent response generation."""
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

    agent = RAGAgent(model="gemini-2.5-flash", retriever=retriever)
    user_query = "What is the process before accepting a motor?"
    response = agent.run(user_query)

    assert response is not None, "RAG agent returned None"
    assert isinstance(response, dict), "RAG agent response should be a dict"

    print("RAG generation test passed!")
    print(f"Response: {response}")

    # Cleanup
    try:
        vector_database.es.indices.delete(index=index_name)
        _log.info(f"Deleted temporary index {index_name}")
    except Exception as e:
        _log.warning(f"Failed to delete temporary index {index_name}: {e}")


if __name__ == "__main__":
    test_generation()
