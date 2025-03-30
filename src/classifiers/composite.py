from typing import List
import logging
from fastapi import UploadFile
from .base import BaseClassifier

# Set up logging
logger = logging.getLogger(__name__)


class CompositeClassifier(BaseClassifier):
    """Composite classifier that combines multiple classifiers."""
    
    def __init__(self, classifiers: List[BaseClassifier]):
        """
        Initialize the composite classifier.
        
        Args:
            classifiers: List of classifiers to use in order
        """
        self.classifiers = classifiers
    
    async def classify(self, file: UploadFile) -> str:
        """
        Classify a file using multiple classifiers in sequence.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            str: The classification result
        """
        for classifier in self.classifiers:
            try:
                result = await classifier.classify(file)
                if result != "unknown file":
                    return result
            except Exception as e:
                logger.error(
                    f"Error in classifier {classifier.__class__.__name__}: "
                    f"{str(e)}"
                )
                continue
        
        return "unknown file" 