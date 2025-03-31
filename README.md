# Heron File Classifier

A robust document classification system that uses multiple classification strategies to identify document types.

## Features

- Multiple classification strategies:
  - Fuzzy string matching
  - Regular expression patterns
  - TF-IDF based classification
  - Filename-based classification
  - Composite classification (weighted voting)
- Support for various file types:
  - PDFs
  - Word documents
  - Excel files
  - Images (with OCR)
  - Text files
- RESTful API with FastAPI
- Docker support for easy deployment

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Make

## Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/heron-file-classifier.git
cd heron-file-classifier
```

2. Create virtual environment and install dependencies:
```bash
make dev
source venv/bin/activate
```

### Docker Setup

1. Build the Docker image:
```bash
make build
```

2. Run the application:
```bash
make run
```

The application will be available at http://localhost:8000

## Usage

### API Endpoints

- `POST /classify_file`: Upload and classify a file
  - Accepts multipart/form-data with a file field
  - Returns classification result with document type and confidence

### Example Request

```bash
curl -X POST "http://localhost:8000/classify_file" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf"
```

### Example Response

```json
{
    "document_type": "bank_statement",
    "classifier_used": "FuzzyClassifier"
}
```

## Testing

Run the test suite:
```bash
make test
```

## Development

### Available Make Commands

- `make dev`: Create virtual environment and install requirements
- `make build`: Build Docker image
- `make run`: Run the application in Docker
- `make test`: Run the test suite
- `make stop`: Stop the Docker containers

### Project Structure

```
heron-file-classifier/
├── src/
│   ├── app.py              # FastAPI application
│   ├── classifiers/        # Classification strategies
│   ├── extractors/         # Text extraction modules
│   ├── models.py           # Data models
│   └── config.py           # Configuration
├── tests/                  # Test suite
├── files/                  # Upload directory
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── Makefile              # Make commands
└── requirements.txt      # Python dependencies
```
