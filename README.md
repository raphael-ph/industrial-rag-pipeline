# industrial-rag-pipeline

**industrial-rag-pipeline** is a Retrieval-Augmented Generation (RAG) pipeline designed for Electrical Motor QA. It integrates document extraction, indexing, retrieval, and generation capabilities using Elasticsearch and Google Generative AI.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the API](#running-the-api)
  - [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project provides a pipeline for processing PDF documents, indexing their content into Elasticsearch, and enabling semantic search and question-answering capabilities. It uses Google Generative AI for embedding generation and response generation.

---

## Features

- **PDF Extraction**: Extracts text from PDF files and splits it into chunks for indexing.
- **Elasticsearch Integration**: Indexes document chunks and performs semantic search using vector embeddings.
- **RAG Agent**: Combines retrieved documents with generative AI to answer user queries.
- **FastAPI**: Provides RESTful endpoints for document indexing and question answering.
- **Logging**: Color-coded logging for better debugging and monitoring.

---

## Installation

### Prerequisites

- Python 3.12 or higher
- Elasticsearch instance
- Google Generative AI API access

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd industrial-rag-pipeline
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` (see [Environment Variables](#environment-variables)).

---

## Usage

### Running the API

1. Start the FastAPI server:
   ```bash
   make run
   ```

2. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Testing

Run all tests using the `Makefile`:
```bash
make test
```

Run specific tests:
- Local integration tests:
  ```bash
  make test-local
  ```
- API tests:
  ```bash
  make test-api
  ```

---

## Environment Variables

The project uses a `.env` file to manage sensitive configurations. Below are the required variables:

```env
# Google API Key
GEMINI_API_KEY="your-google-api-key"

# Elasticsearch configs
ELASTIC_SEARCH_API_KEY="your-elasticsearch-api-key"
ELASTIC_SEARCH_URL="your-elasticsearch-url"
```

---

## Endpoints

### Health Check
- **GET** `/health`
  - Returns the health status of the API.

### Document Indexing
- **POST** `/documents/`
  - Uploads and indexes PDF documents into Elasticsearch.

### Question Answering
- **POST** `/question/`
  - Generates answers to user queries using the RAG pipeline.

---