import logging
from fastapi import UploadFile
from .base import BaseClassifier
from ..models import ClassifierResult

# Set up logging
logger = logging.getLogger(__name__)


class FilenameClassifier(BaseClassifier):
    """Classifier that uses filename patterns to classify files."""
    
    def __init__(self):
        # Keywords and patterns for each document type
        self.patterns = {
            "drivers_licence": [
                "drivers license",
                "driver's license",
                "drivers licence",
                "driver's licence",
                "driving license",
                "driving licence",
                "dl",
                "license",
                "licence",
                "permit",
                "id card",
                "identification",
                "driver id",
                "driver identification"
            ],
            "bank_statement": [
                "bank statement",
                "account statement",
                "banking statement",
                "statement of account",
                "account summary",
                "bank summary",
                "transaction history",
                "account history",
                "banking summary",
                "statement",
                "bank account",
                "account details",
                "banking details",
                "transaction summary"
            ],
            "invoice": [
                "invoice",
                "bill",
                "receipt",
                "payment",
                "charge",
                "fee",
                "cost",
                "amount due",
                "total amount",
                "price",
                "quote",
                "estimate",
                "statement",
                "debit note",
                "credit note",
                "order",
                "purchase order",
                "sales order"
            ]
        }
    
    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file based on its filename.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            ClassifierResult: The classification result
        """
        try:
            filename = self._get_filename(file)
            logger.info(f"Classifying file: {filename}")
            
            # Check each document type's patterns
            for doc_type, patterns in self.patterns.items():
                for pattern in patterns:
                    if pattern in filename:
                        logger.info(
                            f"Classified as '{doc_type}' using pattern "
                            f"'{pattern}'"
                        )
                        return ClassifierResult(
                            document_type=doc_type,
                            classifier_name=self.__class__.__name__
                        )
            
            logger.info("No matching patterns found, returning unknown")
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            )
            
        except Exception as e:
            logger.error(f"Error during filename classification: {str(e)}")
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            ) 