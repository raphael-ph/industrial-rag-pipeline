from elasticsearch import Elasticsearch
from typing import List, Dict
from google import genai
from google.genai import types

# internal imports
from ..utils.logger import Logger

_log = Logger.get_logger(__name__)
google_client = genai.Client()

class ElasticRetriever:
    """Retriver for getting documents stored in a Vector DB

    ElasticRetriever provides semantic search capabilities by combining Google Generative AI 
    embeddings with Elasticsearch vector search. It allows retrieving the most relevant 
    documents from an Elasticsearch index based on semantic similarity to a given query.

    Attributes:
        index_name (str): Name of the Elasticsearch index where documents are stored.
        embedding_model (str): The Google GenAI model used to generate embeddings (default: "gemini-embedding-001").
        embedding_dim (int): Dimensionality of the embedding vectors (default: 768).
        es (Elasticsearch): Elasticsearch client instance used to perform search queries.
    """

    def __init__(
        self,
        elastic_url: str,
        api_key: str,
        index_name: str,
        embedding_model: str = "gemini-embedding-001",
        embedding_dim: str = 768,
    ):
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.embedding_dim = embedding_dim

        # Connect to Elasticsearch
        self.es = Elasticsearch(elastic_url, api_key=api_key)
        _log.info(f"Connected to Elasticsearch at {elastic_url}")

    def retrieve(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve top-k most similar documents using precomputed embeddings.
        Returns a list of dicts with 'title', 'text', and 'score'.
        """
        _log.info(f"Running vector search | Top-K: {top_k} | Query: {query_text[:50]}...")

        # Generate query embedding locally

        query_embedding = self._generate_embeddings(query_text)

        # Use script_score to compute similarity (cosineSimilarity)
        query_body = {
            "size": top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},  # search all docs
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding.values')",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }

        response = self.es.search(index=self.index_name, body=query_body)

        hits = response.get("hits", {}).get("hits", [])
        _log.info(f"Retrieved {len(hits)} results for query.")

        # Extract title, text, and score
        results = [
            {
                "title": hit["_source"]["title"],
                "text": hit["_source"]["text"],
                "score": hit["_score"]
            }
            for hit in hits
        ]

        return results

    def _generate_embeddings(self, text: str) -> List[float]:
        response = google_client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="SEMANTIC_SIMILARITY",
                    output_dimensionality=self.embedding_dim,)
            ).embeddings
        
        embedding_values = response[0].values

        return embedding_values