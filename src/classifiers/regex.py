from typing import Dict, List
import re
import logging
from fastapi import UploadFile
from .base import BaseClassifier
from ..models import ClassifierResult

# Set up logging
logger = logging.getLogger(__name__)


class RegexClassifier(BaseClassifier):
    """Classifier that uses regex patterns to identify document types."""
    
    def __init__(self):
        self.patterns: Dict[str, List[str]] = {
            "drivers_licence": [
                r"drivers?\s*licen[sc]e",
                r"dl\s*number",
                r"driver\s*id",
                r"drivers?\s*permit"
            ],
            "bank_statement": [
                r"bank\s*statement",
                r"account\s*statement",
                r"transaction\s*history",
                r"account\s*summary",
                r"balance\s*sheet",
                r"account\s*balance",
                r"statement\s*period"
            ],
            "invoice": [
                r"invoice",
                r"bill\s*to",
                r"amount\s*due",
                r"payment\s*terms",
                r"invoice\s*number",
                r"invoice\s*date"
            ]
        }
    
    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file based on regex patterns in its content.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            str: The classification result
        """
        try:
            # Get the appropriate extractor for the file type
            from ..extractors.factory import TextExtractorFactory
            extractor = TextExtractorFactory.get_extractor(file)
            
            # Extract text from the file
            text = await extractor.extract_text(file)
            logger.info(f"Extracted text from file: {file.filename}")
            
            # Convert text to lowercase for case-insensitive matching
            text = text.lower()
            
            # Check for patterns in the text
            for doc_type, doc_patterns in self.patterns.items():
                for pattern in doc_patterns:
                    if re.search(pattern, text):
                        logger.info(
                            f"Found pattern '{pattern}' for document type "
                            f"'{doc_type}'"
                        )
                        return ClassifierResult(
                            document_type=doc_type,
                            classifier_name=self.__class__.__name__
                        )
            
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            ) 
            
        except Exception as e:
            logger.error(f"Error during regex classification: {str(e)}")
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            ) 