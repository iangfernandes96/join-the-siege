from typing import List
import logging
from fastapi import UploadFile
from .base import BaseClassifier
from ..models import ClassifierResult

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

    async def classify(self, filename: str, content: str) -> ClassifierResult:
        """
        Classify a file using multiple classifiers in sequence.

        Args:
            file: The file to classify

        Returns:
            ClassifierResult: The first valid classification result
        """
        for classifier in self.classifiers:
            try:
                result = await classifier.classify(filename, content)
                if result.document_type != "unknown":
                    return ClassifierResult(
                        document_type=result.document_type,
                        classifier_name=result.classifier_name,
                    )
            except Exception as e:
                logger.error(
                    f"Error in classifier {classifier.__class__.__name__}: " f"{str(e)}"
                )
                continue

        # If no classifier succeeded, return unknown
        return ClassifierResult(classifier_name=self.__class__.__name__)
