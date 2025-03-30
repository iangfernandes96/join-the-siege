from fastapi import UploadFile
from .classifiers.regex import RegexClassifier
from .classifiers.filename import FilenameClassifier
from .classifiers.tfidf import TFIDFClassifier
# from .classifiers.bert import BERTClassifier
from .classifiers.fuzzy import FuzzyClassifier
from .classifiers.composite import CompositeClassifier
from .models import ClassificationResponse
from .config import config


classifier = CompositeClassifier([
    # RegexClassifier(),
    # BERTClassifier(),
    # TFIDFClassifier(),
    # FuzzyClassifier(),
    FilenameClassifier()
])


async def classify_file(file: UploadFile) -> ClassificationResponse:
    """
    Classify a file using the composite classifier.
    
    Args:
        file: The uploaded file to classify
        
    Returns:
        ClassificationResponse: The classification result with metadata
    """
    result = await classifier.classify(file)
    return ClassificationResponse(
        document_type=result.document_type,
        classifier_name=result.classifier_name
    )
