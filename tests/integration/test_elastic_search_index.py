import os
from dotenv import load_dotenv

# internal imports
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager
from app.utils.logger import Logger

_log = Logger.get_logger(__name__)

load_dotenv()
elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]

_log.debug(f"ELASTIC API KEY: {elastic_api_key}")
_log.debug(f"ELASTIC CLOUD ID: {elastic_url}")

pdf_path = "tests/samples/LB5001.pdf"

vector_database = ElasticVectorManager(
    elastic_url=elastic_url,
    api_key=elastic_api_key,
    index_name="industrial-rag-index",
)

reader = PdfReader()

def test_indexing():
    docs = reader.read(pdf_path)
    vector_database.index_documents(docs)

if __name__ == "__main__":
    test_indexing()