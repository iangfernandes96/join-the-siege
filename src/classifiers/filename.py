from typing import Dict, List
import logging
from fastapi import UploadFile
from .base import BaseClassifier

# Set up logging
logger = logging.getLogger(__name__)


class FilenameClassifier(BaseClassifier):
    """Classifier that uses filename patterns to identify document types."""
    
    def __init__(self):
        self.patterns: Dict[str, List[str]] = {
            "drivers_licence": [
                "drivers_license",
                "drivers_licence",
                "dl",
                "drivers_permit"
            ],
            "bank_statement": [
                "bank_statement",
                "account_statement",
                "statement",
                "banking_statement"
            ],
            "invoice": [
                "invoice",
                # "bill",
                # "receipt",
                # "payment"
            ]
        }
    
    async def classify(self, file: UploadFile) -> str:
        """
        Classify a file based on its filename.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            str: The classification result
        """
        try:
            filename = self._get_filename(file)
            
            # Check for patterns in the filename
            for doc_type, doc_patterns in self.patterns.items():
                if any(pattern in filename for pattern in doc_patterns):
                    logger.info(
                        f"Found filename pattern for document type '{doc_type}'"
                    )
                    return doc_type
            
            return "unknown file"
            
        except Exception as e:
            logger.error(f"Error during filename classification: {str(e)}")
            return "unknown file" 