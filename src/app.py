from fastapi import FastAPI, UploadFile, File, HTTPException
from src.classifier import classify_file
from src.models import (ClassificationError, ClassificationResponse)
from src.utils.request_validation import validate_file
from typing import List
import asyncio

from src.db.in_memory import InMemoryDB

app = FastAPI(
    title="Heron File Classifier",
    description="API for classifying files based on content and metadata",
    version="1.0.0",
)

db = InMemoryDB()


@app.post("/classify_file", response_model=ClassificationResponse)
async def classify_file_route(file: UploadFile = File(default=None)):
    """
    Classify a file into a document type.

    Args:
        file: The file to classify; Maximum file size is 10MB

    Returns:
        ClassificationResponse: Classification result with document type and metadata
    """
    try:
        file = await validate_file(file)
    except Exception as e:
        # raise HTTPException(status_code=400, detail=str(e))
        error = ClassificationError(error="File validation failed", details=str(e))
        # raise HTTPException(status_code=400, detail=error.model_dump())
        return ClassificationResponse(
            document_type="unknown",
            classifier_name="FileValidationClassifier",
            file_name=file.filename,
            error=error.error,
            details=error.details
        )
    try:
        result = await classify_file(file)
        await db.save_classification(result)
        return result
    except Exception as e:
        error = ClassificationError(error="Classification failed", details=str(e))
        raise HTTPException(status_code=500, detail=error.model_dump())


@app.post("/classify_file_bulk", response_model=List[ClassificationResponse])
async def classify_file_bulk_route(files: List[UploadFile] = File(default=None)):
    """
    Classify multiple files at once.
    """
    return await asyncio.gather(*[classify_file_route(file) for file in files])


@app.get("/get_classification", response_model=ClassificationResponse)
async def get_classification_route(file_id: str):
    result = await db.get_classification(file_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Classification not found")
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4,
        loop="uvloop",
        limit_concurrency=1000,
        timeout_keep_alive=30,
        access_log=True,
    )
