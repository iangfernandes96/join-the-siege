from fastapi import UploadFile, HTTPException
from ..config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


async def file_size_check(file: UploadFile) -> bool:
    """Check if the file size is allowed."""
    file.file.seek(0, 2)  # Move to the end of the file
    file_size = file.file.tell()  # Get current position (file size)
    file.file.seek(0)  # Reset position for classification
    return file_size <= MAX_FILE_SIZE_MB * 1024 * 1024


async def validate_file(file: UploadFile) -> UploadFile:
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
            detail=f"File {file.filename} too large. Maximum size is {MAX_FILE_SIZE_MB}MB",
        )
    return file
