from pydantic import BaseModel, Field
from typing import Optional, List

# --- Indexing components ---
class Document(BaseModel):
    """Base class representing a Document chunk to be indexed in Elasticsearch"""
    document_id: str = Field(..., description="Unique id for the document")
    user_id: str = Field(..., description="Unique user id associated with the document")
    title: str = Field(..., description="Original document title or filename.")
    chunk_id: int = Field(..., description="Sequential ID for the chunk within the document")
    text: str = Field(..., description="The actual chunk content")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding for semantic search")
    source_file: Optional[str] = Field(None, description="Original file path or identifier")
    page_number: Optional[int] = Field(None, description="Page number in the original document (if applicable)")


# --- Retrieval coomponents ---
class RAGReference(BaseModel):
    """Base object for holding the references to a generated response"""
    reference_title: str = Field(..., description="The title of the referenced chunk or document.")
    reference_excerpt: List[str] = Field(..., description="The exact excert that was used to generate that specific part of the response.")

class RAGResponse(BaseModel):
    """Base model for structured RAG response generation"""
    reference: List[RAGReference] = Field(..., description="A list of all excerpts and title references used to generate the response.")