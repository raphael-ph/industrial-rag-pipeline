import pymupdf
from uuid import uuid4
from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

# getting current datetime for file saving
current_datetime = datetime.now()
formatted_current_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

# internal imports
from ..schemas.schema import Document
from ..utils.logger import Logger

_log = Logger.get_logger(__name__)

class PdfReader(BaseModel):
    """Reader is linked to the user and session."""
    user_id: Optional[str] = None
    chunk_size: int = 300
    chunk_overlap: int = 50

    def read(self, pdf_source: Union[str, bytes], original_filename: Optional[str] = None) -> List[Document]:
        """Extract text from PDFs and return configured chunks for indexing"""
        doc_id = str(uuid4())
        _log.info(
            f"Starting PDF read | user_id={self.user_id or 'unknown_user'} | "
            f"doc_id={doc_id} | chunk_size={self.chunk_size} | chunk_overlap={self.chunk_overlap}"
        )

        # find PDF source type
        if isinstance(pdf_source, str):
            _log.debug(f"PDF source type: path | path={pdf_source}")
            pdf_doc = pymupdf.open(pdf_source)
            title = pdf_source.split("/")[-1]
            source_file = pdf_source

        elif isinstance(pdf_source, bytes):
            _log.debug(f"PDF source type: bytes | original_filename={original_filename}")
            pdf_doc = pymupdf.open(stream=pdf_source, filetype="pdf")
            title = original_filename or f"uploaded_file_{formatted_current_datetime}.pdf"
            source_file = original_filename or "uploaded_bytes.pdf"

        else:
            _log.error(f"Invalid pdf_source type: {type(pdf_source).__name__}")
            raise ValueError("pdf_source must be a file path or bytes")

        all_documents: List[Document] = []
        chunk_id = 0
        total_pages = len(pdf_doc)
        _log.info(f"Opened PDF successfully | title={title} | pages={total_pages}")

        for page_num, page in enumerate(pdf_doc, start=1):
            _log.debug(f"Processing page {page_num}/{total_pages}")
            text = page.get_text("text")

            if not text.strip():
                _log.warning(f"Page {page_num} contains no extractable text. Skipping.")
                continue

            chunks = self._chunk_text(text)
            _log.debug(
                f"Page {page_num}: extracted {len(chunks)} chunks | "
                f"avg_chunk_length={sum(len(c) for c in chunks) / len(chunks):.1f} chars"
            )

            for chunk_text in chunks:
                if not chunk_text.strip():
                    _log.debug(f"Skipping empty chunk on page {page_num}")
                    continue

                doc = Document(
                    document_id=doc_id,
                    title=title,
                    user_id=self.user_id or "unknown_user",
                    chunk_id=chunk_id,
                    text=chunk_text,
                    source_file=source_file,
                    page_number=page_num
                )
                all_documents.append(doc)
                _log.debug(f"Added chunk {chunk_id} from page {page_num} | length={len(chunk_text)} chars")
                chunk_id += 1

        _log.info(
            f"Completed PDF read | total_chunks={len(all_documents)} | "
            f"total_pages_processed={total_pages} | doc_id={doc_id}"
        )
        return all_documents

    def _chunk_text(self, text: str) -> List[str]:
        """Splits text into overlapping chunks by word count."""
        words = text.split()
        total_words = len(words)
        _log.debug(f"Chunking text | total_words={total_words}")

        chunks = []
        start = 0
        while start < total_words:
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            start += self.chunk_size - self.chunk_overlap

        _log.debug(f"Generated {len(chunks)} chunks from text")
        return chunks
