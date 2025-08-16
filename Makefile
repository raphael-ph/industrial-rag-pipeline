# Variables
UVICORN_CMD = uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Run all local integration tests (direct Python classes)
test-local:
	@echo "Running local integration tests..."
	PYTHONPATH=. python tests/integration/test_pdf_reader.py
	PYTHONPATH=. python tests/integration/test_elastic_search_index.py
	PYTHONPATH=. python tests/integration/test_elastic_search_retrieve.py
	PYTHONPATH=. python tests/integration/test_generation_agent.py
	@echo "All local tests completed!"

# Run API tests (requires API server running)
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


# Run all tests
test: test-local test-api


# Run all integration tests
test: test-local test-api
	@echo "All integration tests completed!"
