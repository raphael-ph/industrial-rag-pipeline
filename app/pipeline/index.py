import time
import random
from typing import List
from dotenv import load_dotenv

# elasticsearch imports
from elasticsearch import Elasticsearch, helpers

# google imports
from google import genai
from google.genai import types

# internal imports
from ..schemas.schema import Document
from ..utils.logger import Logger

_log = Logger.get_logger(__name__)

# configure google client
load_dotenv(".env")
google_client = genai.Client()

class ElasticVectorManager:
    """Indexes Documents into Elasticsearch, generates embeddings via Google AI."""

    def __init__(
        self,
        elastic_url: str,
        api_key: str,
        index_name: str,
        embedding_model: str = "gemini-embedding-001",
        embedding_dim: int = 768
    ):
        self.elastic_url = elastic_url
        self.api_key = api_key
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.embedding_dim = embedding_dim

        # Initialize Elasticsearch client
        self.es = Elasticsearch(self.elastic_url, api_key=self.api_key)
        _log.info(f"Connected to Elasticsearch at {self.elastic_url}")

        # Only create the index if it does not exist
        if not self.es.indices.exists(index=self.index_name):
            _log.info(f"Index '{self.index_name}' did not exist. Creating index...")
            self._create_index()
        else:
            _log.info(f"Index '{self.index_name}' already exists. Skipping creation.")

    def index_documents(self, documents: List[Document]):
        """Generate embeddings for chunks and bulk index to Elasticsearch with retry + backoff."""
        _log.info(f"Starting embedding generation | Total documents to analyze: {len(documents)}")
        actions = []

        for i, doc in enumerate(documents):
            _log.debug(
                f"Generating embeddings for document {i+1}/{len(documents)} | "
                f"Doc Title: {doc.title} | Doc Text: {doc.text[:100]}..."
            )

            # retry loop for embeddings
            max_retries = 10
            backoff = 1  # seconds
            embedding = None

            for attempt in range(max_retries):
                try:
                    embedding = google_client.models.embed_content(
                        model=self.embedding_model,
                        contents=doc.text,
                        config=types.EmbedContentConfig(
                            title=doc.title,
                            task_type="RETRIEVAL_DOCUMENT",
                            output_dimensionality=self.embedding_dim,
                        )
                    ).embeddings[0].values
                    break 
                except Exception as e:
                    wait_time = backoff * (2 ** attempt) + random.uniform(0, 1)
                    _log.warning(
                        f"Rate limit hit (attempt {attempt+1}/{max_retries}). "
                        f"Retrying in {wait_time:.2f}s..."
                    )
                    time.sleep(wait_time)

            if embedding is None:
                _log.error(f"Failed to generate embedding for doc {doc.document_id} after {max_retries} retries")
                raise Exception("Embedding generation failed after retries")

            doc.embedding = embedding
            actions.append({
                "_index": self.index_name,
                "_id": f"{doc.user_id}_{doc.document_id}_{doc.chunk_id}",
                "_source": doc.model_dump()
            })

        _log.info("Embedding generation completed successfully!")
        _log.info(f"Starting bulk index to {self.index_name}...")

        try:
            helpers.bulk(self.es, actions)
            _log.info(f"Indexed {len(documents)} documents into '{self.index_name}'.")
        except Exception as e:
            _log.error(f"Failed to complete document indexing: {e}")
            raise Exception(f"Failed to complete document indexing: {e}")

    
    def _create_index(self):
        """Internal method for creating Elasticsearch index with mapping for text + embeddings."""
        mapping = {
            "mappings": {
                "properties": {
                    "document_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "user_id": {"type": "keyword"},
                    "session_id": {"type": "keyword"},
                    "chunk_id": {"type": "integer"},
                    "text": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": self.embedding_dim},
                    "source_file": {"type": "keyword"},
                    "page_number": {"type": "integer"}
                }
            }
        }
        try:
            self.es.indices.create(index=self.index_name, body=mapping)
            _log.info(f"Successfully created index '{self.index_name}'")
        except Exception as e:
            _log.error(f"Failed to create index '{self.index_name}': {e}")
            raise Exception(f"Failed to create index '{self.index_name}': {e}")
