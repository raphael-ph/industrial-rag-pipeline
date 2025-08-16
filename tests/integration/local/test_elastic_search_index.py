import os
import uuid
from dotenv import load_dotenv
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager
from app.utils.logger import Logger

load_dotenv()
_log = Logger.get_logger(__name__)

elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
pdf_path = "tests/samples/LB5001.pdf"

def test_indexing():
    index_name = f"test-index-{uuid.uuid4().hex[:8]}"
    vector_database = ElasticVectorManager(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=index_name,
    )

    reader = PdfReader()
    docs = reader.read(pdf_path)
    try:
        vector_database.index_documents(docs)
    except:
        _log.info(f"Failed to index documents. Deleting temporary index {index_name}")
        vector_database.es.indices.delete(index=index_name)

    # Verify documents exist in the index
    for doc in docs:
        composite_id = f"{doc.user_id}_{doc.document_id}_{doc.chunk_id}"
        resp = vector_database.es.get(index=index_name, id=composite_id, ignore=[404])
        assert resp["found"], f"Document {composite_id} not found in index!"

    print(f"Indexing test passed! Indexed {len(docs)} documents in {index_name}")

    # Cleanup
    try:
        vector_database.es.indices.delete(index=index_name)
        _log.info(f"Deleted temporary index {index_name}")
    except Exception as e:
        _log.warning(f"Failed to delete temporary index {index_name}: {e}")

if __name__ == "__main__":
    test_indexing()
