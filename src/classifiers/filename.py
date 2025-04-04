import logging
from fastapi import UploadFile
from .base import BaseClassifier
from ..models import ClassifierResult
from ..config import config
from ..utils.decorators import handle_classifier_errors

logger = logging.getLogger(__name__)


class FilenameClassifier(BaseClassifier):
    """Classifier that uses filename patterns to classify files."""

    def __init__(self):
        # Keywords and patterns for each document type
        self.patterns = config.patterns.model_dump()

    @handle_classifier_errors
    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file based on its filename.

        Args:
            file: The uploaded file to classify

        Returns:
            ClassifierResult: The classification result
        """
        filename = self._get_filename(file)

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
