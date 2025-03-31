import logging
from fastapi import UploadFile
from .classifiers.regex import RegexClassifier
from .classifiers.filename import FilenameClassifier
from .classifiers.tfidf import TFIDFClassifier
# from .classifiers.bert import BERTClassifier
from .classifiers.fuzzy import FuzzyClassifier
from .classifiers.composite import CompositeClassifier
from .models import ClassificationResponse, ClassifierResult
from .config import config

logger = logging.getLogger(__name__)

# Initialize classifiers in order of preference
classifiers = [
    FilenameClassifier(),  # Fastest, based on filename patterns
    FuzzyClassifier(),     # Good for similar text patterns
    RegexClassifier(),     # Pattern matching
    TFIDFClassifier(),     # Most complex but potentially most accurate
]


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
    for classifier in classifiers:
        try:
            result = await classifier.classify(file)
            
            # Skip if result is unknown
            if result.document_type == "unknown":
                logger.debug(
                    f"{classifier.__class__.__name__} returned unknown, "
                    "trying next classifier"
                )
                continue
            
            logger.info(
                f"Successful classification from "
                f"{classifier.__class__.__name__}: {result.document_type}"
            )
            
            return ClassificationResponse(
                document_type=result.document_type,
                classifier_name=classifier.__class__.__name__
            )
            
        except Exception as e:
            logger.error(
                f"Error in {classifier.__class__.__name__}: {str(e)}"
            )
            continue
    
    # If we get here, all classifiers failed
    logger.warning("All classifiers failed to classify the file")
    return ClassificationResponse(
        document_type="unknown",
        classifier_name="SequentialClassifier"
    )
