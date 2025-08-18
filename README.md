# industrial-rag-pipeline

**industrial-rag-pipeline** is a Retrieval-Augmented Generation (RAG) pipeline designed for Electrical Motor QA. It integrates document extraction, indexing, retrieval, and generation capabilities using Elasticsearch and Google Generative AI.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the API](#running-the-api)
  - [Running the Playground](#running-the-playground)
  - [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Endpoints](#endpoints)

---

## Overview

This project provides a pipeline for processing PDF documents, indexing their content into Elasticsearch, and enabling semantic search and question-answering capabilities. It uses Google Generative AI for embedding generation and response generation.

---

## Features

- **PDF Extraction**: Extracts text from PDF files and splits it into chunks for indexing.
- **Elasticsearch Integration**: Indexes document chunks and performs semantic search using vector embeddings.
- **RAG Agent**: Combines retrieved documents with generative AI to answer user queries.
- **FastAPI**: Provides RESTful endpoints for document indexing and question answering.
- **Streamlit Playground**: Interactive interface for testing the RAG pipeline.
- **Logging**: Color-coded logging for better debugging and monitoring.

---

## Project Structure

```plaintext
.
├── api/                # FastAPI endpoints for the RAG pipeline
├── app/                # Core application logic (pipeline, prompts, schemas, utils)
├── notebooks/          # Jupyter notebooks for evaluation and experimentation
├── tests/              # Unit and integration tests
├── playground.py       # Streamlit app for interactive RAG testing
├── Makefile            # Automation scripts for development and testing
├── .env                # Environment variables (not included in version control)
├── pyproject.toml      # Project dependencies and metadata
└── README.md           # Project documentation
```

---

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Elasticsearch instance
- Google Generative AI API access

### Steps

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip
   pip install uv
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd industrial-rag-pipeline
   ```

3. **Create and activate virtual environment with uv**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv sync
   ```

5. **Set up environment variables** in `.env` (see [Environment Variables](#environment-variables)).

---

## Usage

### Running the API

1. Start the FastAPI server:
   ```bash
   make dev
   ```
   
   Or directly with uv:
   ```bash
   uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Running the Playground

1. Start the Streamlit playground:
   ```bash
   make playground
   ```
   
   Or directly with uv:
   ```bash
   uv run streamlit run playground.py
   ```

2. Open the playground in your browser:
   - [http://localhost:8501](http://localhost:8501)

### Testing

Run all tests using the `Makefile`:
```bash
make test
```

Run specific tests:
- Local integration tests:
  ```bash
  make test-local
  # Or: uv run pytest tests/local/
  ```
- API tests:
  ```bash
  make test-api
  # Or: uv run pytest tests/api/
  ```

---

## Development

### Adding Dependencies

Add new dependencies using uv:

```bash
# Add a regular dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Add from a specific source
uv add "package-name>=1.0.0"
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update a specific package
uv add --upgrade package-name
```

### Running Scripts

Use `uv run` to execute scripts within the project environment:

```bash
# Run Python scripts
uv run python scripts/your_script.py

# Run CLI tools
uv run black .
uv run isort .
uv run mypy .
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

# Optional
INDEX_NAME="your-default-index-name"
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

## Why UV?

This project uses [uv](https://docs.astral.sh/uv/) as the Python package manager for several advantages:

- **Speed**: 10-100x faster than pip for dependency resolution and installation
- **Reliability**: Consistent dependency resolution with lockfile support
- **Simplicity**: Single tool for virtual environments, dependency management, and script running
- **Modern**: Built with Rust for performance and reliability
- **Compatibility**: Works with existing `pyproject.toml` and `requirements.txt` files

If you prefer using pip, you can still generate a requirements file:
```bash
uv export --format requirements-txt --output-file requirements.txt
```