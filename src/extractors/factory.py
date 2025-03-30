from typing import Dict, Type
from fastapi import UploadFile
from .base import BaseTextExtractor
from .pdf import PDFExtractor
from .docx import DocxExtractor
from .excel import ExcelExtractor
from .image import ImageExtractor
from .text import TextExtractor


class TextExtractorFactory:
    """Factory class for managing text extractors."""
    
    # Map file extensions to their corresponding extractors
    _extractors: Dict[str, Type[BaseTextExtractor]] = {
        'pdf': PDFExtractor,
        'docx': DocxExtractor,
        'doc': DocxExtractor,  # Handle both .doc and .docx
        'xlsx': ExcelExtractor,
        'xls': ExcelExtractor,  # Handle both .xls and .xlsx
        'png': ImageExtractor,
        'jpg': ImageExtractor,
        'jpeg': ImageExtractor,
        'txt': TextExtractor,
        'csv': TextExtractor,  # Treat CSV as text
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
            
            # Map MIME types to extensions
            mime_to_extension = {
                'application/pdf': 'pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                'application/msword': 'doc',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
                'application/vnd.ms-excel': 'xls',
                'text/plain': 'txt',
                'text/csv': 'csv'
            }
            
            # If we have a valid MIME type, use it
            if mime_type in mime_to_extension:
                extension = mime_to_extension[mime_type]
            # For images, keep the original extension
            elif mime_type.startswith('image/'):
                pass
            else:
                raise ValueError(f"Unsupported MIME type: {mime_type}")
                
        except ImportError:
            # If python-magic is not available, just use the file extension
            pass
        except Exception as e:
            # If there's any other error with python-magic, fall back to extension
            print(f"Warning: Failed to use python-magic: {str(e)}")
        
        # Get the appropriate extractor based on extension
        if extension in cls._extractors:
            return cls._extractors[extension]()
            
        raise ValueError(f"Unsupported file extension: {extension}") 