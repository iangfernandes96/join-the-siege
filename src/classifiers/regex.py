import re
import logging
from fastapi import UploadFile
from .base import BaseClassifier
from ..models import ClassifierResult
from ..config import config
from ..extractors.factory import TextExtractorFactory

logger = logging.getLogger(__name__)


class RegexClassifier(BaseClassifier):
    """Classifier that uses regex patterns to identify document types."""

    def __init__(self):
        self.patterns = config.regex_patterns.model_dump()

    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file based on regex patterns in its content.

        Args:
            file: The uploaded file to classify

        Returns:
            str: The classification result
        """
        try:
            extractor = TextExtractorFactory.get_extractor(file)
            text = await extractor.extract_text(file)

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
                            classifier_name=self.__class__.__name__,
                        )

            return ClassifierResult(classifier_name=self.__class__.__name__)

        except Exception as e:
            logger.error(f"Error during regex classification: {str(e)}")
            return ClassifierResult(classifier_name=self.__class__.__name__)
