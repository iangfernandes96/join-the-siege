from fastapi import FastAPI, UploadFile, File, HTTPException
from src.classifier import classify_file
from src.models import (ClassificationError, ClassificationResponse)
from src.utils.request_validation import validate_file


app = FastAPI(
    title="Heron File Classifier",
    description="API for classifying files based on content and metadata",
    version="1.0.0",
)


@app.post("/classify_file", response_model=ClassificationResponse)
async def classify_file_route(file: UploadFile = File(default=None)):
    """
    Classify a file into a document type.

    Args:
        file: The file to classify; Maximum file size is 10MB

    Returns:
        ClassificationResponse: Classification result with document type and metadata
    """
    file = await validate_file(file)
    try:
        result = await classify_file(file)
        return result
    except Exception as e:
        error = ClassificationError(error="Classification failed", details=str(e))
        raise HTTPException(status_code=500, detail=error.model_dump())


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
