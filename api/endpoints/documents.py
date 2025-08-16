import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager
from app.utils.logger import Logger
from dotenv import load_dotenv

load_dotenv()
_log = Logger.get_logger(__name__)

elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]

router = APIRouter()

@router.post("/")
async def index_documents(
    user_id: str = Form(...),
    session_id: str = Form(...),
    index_name: Optional[str] = Form(None),
    files: List[UploadFile] = File(...)
):
    """
    Index one or more PDF documents into Elasticsearch with user/session info.
    Optional index_name can be provided; otherwise a random one is generated.
    Returns number of documents processed and total chunks.
    """
    if not index_name:
        index_name = f"index-{user_id}-{session_id}"

    vector_database = ElasticVectorManager(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=index_name,
    )

    total_docs = 0
    total_chunks = 0

    for file in files:
        pdf_content = await file.read()
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(pdf_content)

        reader = PdfReader()
        docs = reader.read(temp_path)

        # Add user_id and session_id to each document
        for doc in docs:
            doc.user_id = user_id
            doc.session_id = session_id

        try:
            vector_database.index_documents(docs)
        except Exception as e:
            _log.info(f"Failed to index documents from {file.filename}. Deleting temporary index {index_name}")
            vector_database.es.indices.delete(index=index_name)
            return {"error": str(e)}

        total_docs += 1
        total_chunks += len(docs)

    return {
        "message": "Documents processed successfully",
        "index_name": index_name,
        "documents_indexed": total_docs,
        "total_chunks": total_chunks
    }
