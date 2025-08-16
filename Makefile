# Run all integration tests
test:
	@echo "Running integration tests..."
	python tests/integration/test_pdf_reader.py
	python tests/integration/test_elastic_search_index.py
	python tests/integration/test_elastic_search_retrieve.py
	python tests/integration/test_generation_agent.py
	@echo "All tests completed!"