from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.classifier import classify_file
from src.models import ClassificationError, ClassificationResponse
from src.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


app = FastAPI(
    title="Heron File Classifier",
    description="API for classifying files based on content and metadata",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@app.post("/classify_file", response_model=ClassificationResponse)
async def classify_file_route(file: UploadFile = File(default=None)):
    """
    Classify a file into a document type.
    
    Args:
        file: The file to classify
        
    Returns:
        ClassificationResponse: Classification result with document type and metadata
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file or filename provided")
    
    if not allowed_file(file.filename):
        allowed = ', '.join(ALLOWED_EXTENSIONS)
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {allowed}"
        )
    
    # Check file size with chunked reading
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB"
            )
    
    # Reset file position for classification
    await file.seek(0)
    
    try:
        result = await classify_file(file)
        return ClassificationResponse(
            document_type=result.document_type,
            classifier_name=result.classifier_name
        )
    except Exception as e:
        error = ClassificationError(
            error="Classification failed",
            details=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=error.model_dump()
        )

# Entry point for Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4,
        loop="uvloop",
        limit_concurrency=1000,
        timeout_keep_alive=30,
        access_log=True
    )
