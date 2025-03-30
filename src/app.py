from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Set
from src.classifier import classify_file

app = FastAPI(
    title="Heron File Classifier",
    description="API for classifying files based on their content and metadata",
    version="1.0.0"
)

ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'png', 'jpg', 'jpeg', 'xls',
                                'xlsx', 'doc', 'docx', 'csv', 'txt'}


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.post("/classify_file")
async def classify_file_route(file: UploadFile) -> JSONResponse:
    """
    Classify a file based on its content and metadata.
    
    Args:
        file: The uploaded file to classify
        
    Returns:
        JSONResponse: Contains the classification result
        
    Raises:
        HTTPException: If file is missing or has invalid extension
    """
    # if not file:
    #     raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    file_class = await classify_file(file)
    return JSONResponse(content={"file_class": file_class})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
