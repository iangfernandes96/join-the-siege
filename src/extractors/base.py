from abc import ABC, abstractmethod
from fastapi import UploadFile


class BaseTextExtractor(ABC):
    """Base class for text extraction from different file types."""
    
    @abstractmethod
    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from the given file.
        
        Args:
            file: The uploaded file to extract text from
            
        Returns:
            str: The extracted text
            
        Raises:
            ValueError: If the file cannot be processed
        """
        pass 