from abc import ABC, abstractmethod
from fastapi import UploadFile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseClassifier(ABC):
    """Base class for all document classifiers."""
    
    @abstractmethod
    async def classify(self, file: UploadFile) -> str:
        """
        Classify a file based on its content and metadata.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            str: The classification result
        """
        pass
    
    def _get_filename(self, file: UploadFile) -> str:
        """
        Get the filename from the uploaded file.
        
        Args:
            file: The uploaded file
            
        Returns:
            str: The filename in lowercase
        """
        if not file or not file.filename:
            raise ValueError("File must have a filename")
        return file.filename.lower() 