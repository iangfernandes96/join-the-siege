from fastapi import FastAPI, UploadFile, File, HTTPException
from src.classifier import classify_file
from src.models import ClassificationError, ClassificationResponse
from src.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from src.utils.request_validation import allowed_file, file_size_check


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
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file or filename provided")

    if not allowed_file(file.filename):
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        raise HTTPException(
            status_code=400, detail=f"File type not allowed. Allowed types: {allowed}"
        )

    if not await file_size_check(file):
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB",
        )

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
