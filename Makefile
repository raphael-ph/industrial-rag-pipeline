# Variables
UVICORN_CMD = uvicorn main:app --reload --host 127.0.0.1 --port 8000

# =============================================================================
# 🚀 Development Server
#
# This target launches the FastAPI development server with hot-reload enabled
# for the RAG (Retrieval-Augmented Generation) API pipeline.
#
# Features:
#   • Health check validation to ensure proper startup
#   • Connected to Elasticsearch index for RAG operations
#
# Usage:
#   make dev
#
# Endpoints:
#   • API Server: http://localhost:8000
#   • Interactive Docs: http://localhost:8000/docs
#   • Health Check: http://localhost:8000/health
#   • Documents: http://localhost:8000/documents
#   • Question: http://localhost:8000/question
# 
#
# Notes:
#   • Ensure Elasticsearch index is populated
#   • Use Ctrl+C to stop the development server
#   • Monitor console logs for debugging and API request insights
# =============================================================================
dev:
	$(UVICORN_CMD) & \
	echo "Starting development server..."; \
	until curl -f http://localhost:8000/health 2>/dev/null; do \
		sleep 1; \
	done; \
	echo "API ready!"; \
	echo "Swagger docs: http://localhost:8000/docs"; \
	echo "Health check: http://localhost:8000/health"; \
	wait

# =============================================================================
# 🧪 Experiments / Playground
#
# This target launches an interactive Streamlit playground for experimenting
# with the RAG (Retrieval-Augmented Generation) pipeline.
#
# Features:
#   • The app is already connected to a pre-populated Elasticsearch index.
#   • You can run queries and explore how the RAG pipeline responds.
#   • Ideal for testing new prompts, embeddings, or analyzing system behavior.
#
# Usage:
#   make playground
#
# Notes:
#   • Ensure your Elasticsearch index is available and populated.
#   • Logs will appear in the console; monitor them for debugging or insights.
# =============================================================================

playground:
	@echo "==============================================================================="
	@echo "| 🚀 Starting your RAG playground...                                          |"
	@echo "|                                                                             |"
	@echo "| 💡 Try asking about a motor specs                                           |"
	@echo "|                                                                             |"
	@echo "| 🔍 IMPORTANT: You are already connected to a valid index!		      |"
	@echo "==============================================================================="
	PYTHONPATH=. python -m streamlit run playground.py

# ========================= Testing ===================================
# All tests in this project are already scripted. This target will:
#   - Start the API
#   - Run all pre-built test suites (unit + integration)
#   - Stream logs to the console in real-time

# Run all local integration tests
test-local:
	@echo "Running local integration tests..."
	PYTHONPATH=. python tests/integration/test_pdf_reader.py
	PYTHONPATH=. python tests/integration/test_elastic_search_index.py
	PYTHONPATH=. python tests/integration/test_elastic_search_retrieve.py
	PYTHONPATH=. python tests/integration/test_generation_agent.py
	@echo "All local tests completed!"

# Run API tests
test-api:
	@echo "Iniciando servidor de desenvolvimento..."
	(uv run $(UVICORN_CMD) & \
		echo "Waiting for API to start..."; \
		until curl -f http://localhost:8000/health 2>/dev/null; do \
			sleep 1; \
		done; \
		echo "API ready! Swagger docs: http://localhost:8000/docs"; \
		echo "Starting /documents test..."; \
		PYTHONPATH=. python tests/integration/api/test_api_documents.py; \
		echo "/documents tests completed!"; \
		echo "Starting /question test..."; \
		PYTHONPATH=. python tests/integration/api/test_api_question.py; \
		echo "/question tests completed!"; \
		echo "All tests completed!" \
		pkill -f uvicorn)

# Run all integration tests
test: test-local test-api
	@echo "All integration tests completed!"
