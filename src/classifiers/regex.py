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
        self.patterns = {
            doc_type: [re.compile(pattern, re.IGNORECASE) for pattern in doc_patterns]
            for doc_type, doc_patterns in config.regex_patterns.model_dump().items()
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
            extractor = TextExtractorFactory.get_extractor(file)
            text = await extractor.extract_text(file)

            # Convert text to lowercase for case-insensitive matching
            text = text.lower()

            for doc_type, regex_patterns in self.patterns.items():
                if any(pattern.search(text) for pattern in regex_patterns):
                    logger.info(f"Classified '{file.filename}' as '{doc_type}'")
                    return ClassifierResult(
                        document_type=doc_type,
                        classifier_name=self.__class__.__name__,
                    )

            return ClassifierResult(classifier_name=self.__class__.__name__)

        except Exception as e:
            logger.error(f"Error during regex classification: {str(e)}")
            return ClassifierResult(classifier_name=self.__class__.__name__)
