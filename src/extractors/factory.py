from typing import Dict, Type
from fastapi import UploadFile
from .base import BaseTextExtractor
from .pdf import PDFExtractor
from .docx import DocxExtractor
from .excel import ExcelExtractor
from .image import ImageExtractor
from .text import TextExtractor
from ..config import config


class TextExtractorFactory:
    """Factory class for managing text extractors."""
    
    # Map file extensions to their corresponding extractors
    _extractors: Dict[str, Type[BaseTextExtractor]] = {
        'pdf': PDFExtractor,
        'docx': DocxExtractor,
        'doc': DocxExtractor,
        'xlsx': ExcelExtractor,
        'xls': ExcelExtractor,
        'png': ImageExtractor,
        'jpg': ImageExtractor,
        'jpeg': ImageExtractor,
        'txt': TextExtractor,
        'csv': ExcelExtractor,
    }
    
    @classmethod
    def get_extractor(cls, file: UploadFile) -> BaseTextExtractor:
        """
        Get the appropriate text extractor for the given file.
        
        Args:
            file: The uploaded file
            
        Returns:
            BaseTextExtractor: The appropriate text extractor
            
        Raises:
            ValueError: If no suitable extractor is found
        """
        # First try to get the file extension
        if not file.filename or '.' not in file.filename:
            raise ValueError("File must have a valid extension")
            
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        # Try to use python-magic if available
        try:
            import magic
            # Read the first 2048 bytes to determine file type
            content = file.file.read(2048)
            file.file.seek(0)  # Reset file pointer
            
            # Use python-magic to determine file type
            mime = magic.Magic(mime=True)
            mime_type = mime.from_buffer(content)
            
            mime_to_extension = config.mime_to_extension
            
            # If we have a valid MIME type, use it
            if mime_type in mime_to_extension:
                extension = mime_to_extension[mime_type]
            # For images, keep the original extension
            elif mime_type.startswith('image/'):
                pass
            else:
                raise ValueError(f"Unsupported MIME type: {mime_type}")
        except Exception as e:
            print(f"Error occurred with mime type checking: {str(e)}")
        
        # Get the appropriate extractor based on extension
        if extension in cls._extractors:
            return cls._extractors[extension]()
            
        raise ValueError(f"Unsupported file extension: {extension}")
