import logging
from fastapi import UploadFile
from .classifiers.regex import RegexClassifier
from .classifiers.filename import FilenameClassifier
from .classifiers.tfidf import TFIDFClassifier
from .classifiers.fuzzy import FuzzyClassifier
from .classifiers.composite import CompositeClassifier
from .models import ClassificationResponse

logger = logging.getLogger(__name__)

# Initialize classifiers in order of preference
classifiers = [
    FilenameClassifier(),
    FuzzyClassifier(),
    RegexClassifier(),
    TFIDFClassifier(),
]

classifier = CompositeClassifier(classifiers)


async def classify_file(file: UploadFile) -> ClassificationResponse:
    """
    Classify a file using a sequence of classifiers with fallback.
    Each classifier is tried in sequence until a valid result is found.
    If all classifiers fail, returns unknown.

    Args:
        file: The uploaded file to classify

    Returns:
        ClassificationResponse: The classification result with metadata
    """
    try:
        result = await classifier.classify(file)
        return ClassificationResponse(
            document_type=result.document_type, classifier_name=result.classifier_name
        )
    except Exception as e:
        logger.error(f"Error in {classifier.__class__.__name__}: {str(e)}")
        logger.warning("All classifiers failed to classify the file")
        return ClassificationResponse(
            document_type="unknown", classifier_name="SequentialClassifier"
        )
