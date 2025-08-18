# App Module

The `app` module is the core of the **Industrial RAG Pipeline**. It contains the main components for document processing, retrieval, and generation, as well as utility functions and schemas.

## Structure

The module is organized into the following subdirectories:

- **`pipeline/`**: Contains the main pipeline components for document extraction, indexing, retrieval, and response generation.
- **`prompts/`**: Stores prompt templates used for the RAG (Retrieval-Augmented Generation) system.
- **`schemas/`**: Defines data models and schemas for documents, responses, and other entities.
- **`utils/`**: Provides utility functions, such as logging.

## Submodules

### `pipeline/`

1. **`extract.py`**: Handles PDF text extraction and chunking for indexing.
2. **`index.py`**: Manages document indexing in Elasticsearch and embedding generation using Google Generative AI.
3. **`retrieve.py`**: Implements semantic search using Elasticsearch and Google embeddings.
4. **`generate.py`**: Combines retrieved documents with generative AI to produce responses.

### `prompts/`

- **`rag.py`**: Contains the default prompt template for the RAG system, ensuring structured and accurate responses.

### `schemas/`

- **`schema.py`**: Defines Pydantic models for documents, RAG responses, and references.

### `utils/`

- **`logger.py`**: Provides a color-coded logging utility for better debugging and monitoring.

## Key Features

- **PDF Extraction**: Extracts text from PDF files and splits it into chunks for indexing.
- **Elasticsearch Integration**: Indexes document chunks and performs semantic search using vector embeddings.
- **RAG Agent**: Combines retrieved documents with generative AI to answer user queries.
- **Logging**: Color-coded logging for better debugging and monitoring.

## Usage

### Example: Extracting and Indexing Documents

```python
from app.pipeline.extract import PdfReader
from app.pipeline.index import ElasticVectorManager

# Extract text from a PDF
reader = PdfReader(user_id="user123", session_id="session456")
documents = reader.read("example.pdf")

# Index documents in Elasticsearch
indexer = ElasticVectorManager(
    elastic_url="https://your-elasticsearch-url",
    api_key="your-api-key",
    index_name="documents-index"
)
indexer.index_documents(documents)
```

### Example: Retrieving and Generating Responses

```python
from app.pipeline.retrieve import ElasticRetriever
from app.pipeline.generate import RAGAgent

# Initialize retriever
retriever = ElasticRetriever(
    elastic_url="https://your-elasticsearch-url",
    api_key="your-api-key",
    index_name="documents-index"
)

# Initialize RAG agent
agent = RAGAgent(
    model="gemini-generation-001",
    retriever=retriever,
    similarity_threshold=0.7
)

# Generate a response
response = agent.run("What are the safety guidelines for motor installation?")
print(response)
```

## Logging

The `Logger` utility provides color-coded logs for better debugging. 

**Important:** Change Logging Level globally at the `utils/logger.py` file.

Example usage:

```python
from app.utils.logger import Logger

log = Logger.get_logger("ExampleApp")
log.info("This is an info message")
log.error("This is an error message")
```

