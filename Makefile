.PHONY: venv install build run test clean

# Create virtual environment
venv:
	python -m venv venv
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
	docker compose build

# Run the application in Docker
run:
	docker compose up

# Run tests
test:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi
	. venv/bin/activate && pytest -v

# Development setup (create venv and install requirements)
dev: venv install

# Stop the application
stop:
	docker compose down 