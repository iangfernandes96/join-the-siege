# Heron File Classifier

A document classification system that uses multiple classification strategies to identify document types.

Please refer to SUBMISSION.md, for a detailed explanation on the submission.

## Features

- Multiple classification strategies:
  - Fuzzy string matching (using rapidfuzz for efficient string similarity)
  - Regular expression patterns (for precise pattern matching)
  - TF-IDF based classification (for semantic similarity)
  - Filename-based classification (fast, pattern-based classification)
- Support for various file types:
  - PDFs
  - Word documents
  - Excel files
  - Images (with OCR)
  - Text files
- RESTful API with FastAPI
- Docker support for easy deployment
- Optimized performance with Uvicorn and uvloop

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Make

## Running the Application
You can run the application either via Docker (recommended) or locally. Follow the instructions below depending on your preferred setup.

### Docker Setup

1. Build the Docker image:
```bash
make build
```

2. Run the application:
```bash
make run
```

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/iangfernandes96/join-the-siege.git
cd heron-file-classifier
```

2. Create virtual environment and install dependencies:
```bash
make dev
```

3. Run app locally
```bash
make run-uvicorn
```
The first time you run the app via `make run-uvicorn`, it may take a few seconds longer to start due to the training for the TF-IDF model. Subsequent startups will be much faster.

The application will be available at http://localhost:8000. API Documentation will be available at http://localhost:8000/docs

## Usage

### API Endpoints

- `POST /classify_file`: Upload and classify a file
  - Accepts multipart/form-data with a file field
  - Returns classification result with document type and classifier used
  - Maximum file size: 10MB
  - Supported file types: PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG

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
    "classifier_name": "FuzzyClassifier"
}
```

## Classification Algorithm

The system uses a sequential classification approach with multiple strategies. The implementations are present in `src/classifiers/`:

1. **Filename Classifier**
   - Fastest classification method
   - Uses pattern matching on filenames
   - Good for files that follow standardized naming conventions

2. **Fuzzy Classifier**
   - Uses rapidfuzz for efficient string similarity matching with filename
   - Good for handling variations in text
   - Handles typos and minor text differences in filenames

3. **Regex Classifier**
   - Precise pattern matching using regular expressions over the file text
   - Good for structured documents
   - Handles specific document formats

4. **TF-IDF Classifier**
   - Most complex but potentially most accurate
   - Uses TF-IDF vectorization for semantic similarity, with Naive-Bayes method of classification
   - Good for content-based classification

The system tries each classifier in sequence until a valid result is found. If all classifiers fail, it returns "unknown" as the document type.

### Local Development
```bash
make run-uvicorn
```
This runs the application with:
- 4 worker processes
- uvloop for better async performance
- 1000 concurrent connections limit
- 30-second keep-alive timeout

### Docker Deployment
The Docker setup includes the same optimizations:
- 4 Uvicorn workers
- uvloop for async performance
- Optimized system dependencies
- Efficient file handling

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
- `make run-uvicorn`: Run the application locally with optimized settings
- `make test`: Run the test suite
- `make stop`: Stop the Docker containers

### Project Structure

```
heron-file-classifier/
├── src/
│   ├── app.py              # FastAPI application
│   ├── classifier.py       # Main classification logic
│   ├── classifiers/        # Classification strategies
│   │   ├── base.py        # Base classifier interface
│   │   ├── fuzzy.py       # Fuzzy matching classifier
│   │   ├── regex.py       # Regex pattern classifier
│   │   ├── tfidf.py       # TF-IDF based classifier
│   │   └── filename.py    # Filename pattern classifier
│   ├── extractors/        # Text extraction modules
│   │   ├── base.py        # Base extractor interface
│   │   ├── docx.py        # Text extractor for docx
│   │   ├── excel.py       # Text extractor for excel
│   │   ├── factory.py     # Extractor for all file types
│   │   └── image.py       # Text extractor for images
│   │   ├── pdf.py         # Text extractor for pdfs
│   │   └── text.py        # Text extractor for text files
│   ├── models.py          # Data models
│   └── config.py          # Configuration
├── tests/                 # Test suite
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── Makefile             # Build and development commands
```
