# API Module

The `api` module provides RESTful endpoints for the **Industrial RAG Pipeline**. It is built using FastAPI and exposes functionality for document indexing, question answering, and health checks.

## Endpoints

### 1. Health Check
- **Path**: `/health`
- **Method**: `GET`
- **Description**: Returns the health status of the API.
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

### 2. Document Indexing
- **Path**: `/documents/`
- **Method**: `POST`
- **Description**: Uploads and indexes PDF documents into Elasticsearch.
- **Request Parameters**:
  - `user_id` (form): User identifier.
  - `session_id` (form): Session identifier.
  - `index_name` (form, optional): Name of the Elasticsearch index. If not provided, a random name is generated.
  - `files` (form): List of PDF files to be indexed.
- **Response**:
  ```json
  {
    "message": "Documents processed successfully",
    "index_name": "index-name",
    "documents_indexed": 2,
    "total_chunks": 10
  }
  ```

### 3. Question Answering
- **Path**: `/question/`
- **Method**: `POST`
- **Description**: Generates answers to user queries using the RAG pipeline.
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "session_id": "string",
    "index_name": "string",
    "question": "string"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "string"
  }
  ```

## Features

- **Health Monitoring**: Simple endpoint to check API status.
- **Document Indexing**: Uploads and processes PDF documents for Elasticsearch indexing.
- **Question Answering**: Combines document retrieval and generative AI to answer user queries.

## Usage

### Running the API
1. Start the FastAPI server:
   ```bash
   make dev
   ```
2. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Testing the API
Run integration tests for the API:
```bash
make test-api
```

## Environment Variables

Ensure the following environment variables are set in the `.env` file:
```env
# Elasticsearch configs
ELASTIC_SEARCH_API_KEY="your-elasticsearch-api-key"
ELASTIC_SEARCH_URL="your-elasticsearch-url"
```