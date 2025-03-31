.PHONY: venv install build run test clean dev stop run-uvicorn

# Create virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Run 'source venv/bin/activate' to activate it."

# Install requirements in virtual environment
install:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Requirements installed successfully."

# Build Docker image
build:
	docker build -t heron-classifier .

# Run the application in Docker
run:
	docker compose up

# Run tests
test:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi
	. venv/bin/activate && python -m pytest tests/ -v

# Development setup (create venv and install requirements)
dev: venv install

# Stop the application
stop:
	docker compose down

# Run the application with Uvicorn (4 workers)
run-uvicorn:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi
	@if [ ! -f "venv/bin/uvicorn" ]; then \
		echo "Uvicorn not found. Installing dependencies..."; \
		. venv/bin/activate && pip install -r requirements.txt; \
	fi
	. venv/bin/activate && uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop --limit-concurrency 1000 --timeout-keep-alive 30 --access-log 