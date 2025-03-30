from fastapi import UploadFile
from .classifiers.regex import RegexClassifier
from .classifiers.filename import FilenameClassifier
from .classifiers.tfidf import TFIDFClassifier
from .classifiers.bert import BERTClassifier
from .classifiers.fuzzy import FuzzyClassifier
from .classifiers.composite import CompositeClassifier
from .models import ClassificationResponse
from .config import config


# Create the composite classifier with all classifiers
classifier = CompositeClassifier([
    RegexClassifier(),
    # BERTClassifier(),
    TFIDFClassifier(),
    FuzzyClassifier(),
    FilenameClassifier()
])


async def classify_file(file: UploadFile) -> dict:
    """
    Classify a file using the composite classifier.
    
    Args:
        file: The uploaded file to classify
        
    Returns:
        dict: The classification result with metadata
    """
    result = await classifier.classify(file)
    return {
        "document_type": result,
        "classifier_used": classifier.__class__.__name__
    }

