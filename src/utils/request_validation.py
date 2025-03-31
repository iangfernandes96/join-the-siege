from fastapi import UploadFile
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
