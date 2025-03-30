from fastapi import FastAPI, UploadFile, File, HTTPException
from src.classifier import classify_file
from src.models import ClassificationError, ClassificationResponse
from src.config import ALLOWED_EXTENSIONS


app = FastAPI(
    title="Heron File Classifier",
    description="API for classifying files based on content and metadata",
    version="1.0.0"
)


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.post("/classify_file", response_model=ClassificationResponse)
async def classify_file_route(file: UploadFile = File(...)):
    """
    Classify a file into a document type.
    
    Args:
        file: The file to classify
        
    Returns:
        ClassificationResponse: Classification result with document type and metadata
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        result = await classify_file(file)
        return result
    except Exception as e:
        error = ClassificationError(
            error="Classification failed",
            details=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=error.dict()
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
