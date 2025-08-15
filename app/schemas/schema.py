from pydantic import BaseModel, Field
from typing import Optional, List

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