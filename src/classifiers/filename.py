import logging
from .base import BaseClassifier
from ..models import ClassifierResult
from ..config import config

logger = logging.getLogger(__name__)


class FilenameClassifier(BaseClassifier):
    """Classifier that uses filename patterns to classify files."""

    def __init__(self):
        # Keywords and patterns for each document type
        self.patterns = config.patterns.model_dump()

    async def classify(self, filename: str, content: str) -> ClassifierResult:
        """
        Classify a file based on its filename.

        Args:
            file: The uploaded file to classify

        Returns:
            ClassifierResult: The classification result
        """
        try:
            # Check each document type's patterns
            for doc_type, patterns in self.patterns.items():
                for pattern in patterns:
                    if pattern in filename:
                        logger.info(
                            f"Classified as '{doc_type}' using pattern " f"'{pattern}'"
                        )
                        return ClassifierResult(
                            document_type=doc_type,
                            classifier_name=self.__class__.__name__,
                        )

            logger.info("No matching patterns found, returning unknown")
            return ClassifierResult(classifier_name=self.__class__.__name__)

        except Exception as e:
            logger.error(f"Error during filename classification: {str(e)}")
            return ClassifierResult(classifier_name=self.__class__.__name__)
