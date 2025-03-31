import logging
from fastapi import UploadFile
from rapidfuzz import process
from .base import BaseClassifier
from ..config import config
from ..models import ClassifierResult

logger = logging.getLogger(__name__)


class FuzzyClassifier(BaseClassifier):
    """Classifier that uses fuzzy string matching to classify files."""
    
    def __init__(self):
        self.patterns = config.patterns.model_dump()
        self.similarity_threshold = config.classifier.similarity_threshold
    
    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file using fuzzy string matching on the filename.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            ClassifierResult: The classification result
        """
        try: 
            filename = self._get_filename(file)
            # Calculate similarity scores for each document type
            best_match = None
            best_score = 0
            
            for doc_type, patterns in self.patterns.items():
                # Get the best matching pattern for this document type
                match = process.extractOne(filename, patterns)
                if match and match[1] > best_score:
                    best_score = match[1]
                    best_match = doc_type
            
            # Return the best match if it exceeds the threshold
            if best_match and best_score >= self.similarity_threshold:
                logger.info(
                    f"Classified as '{best_match}' with similarity "
                    f"score {best_score:.1f}"
                )
                return ClassifierResult(
                    document_type=best_match,
                    classifier_name=self.__class__.__name__
                )
            
            # If no good match found, try partial matching
            # Can be skipped, since we are running Filename matching first
            for doc_type, patterns in self.patterns.items():
                for pattern in patterns:
                    # Check if the pattern is contained within the filename
                    if pattern in filename:
                        logger.info(
                            f"Classified as '{doc_type}' using partial "
                            f"match with '{pattern}'"
                        )
                        return ClassifierResult(
                            document_type=doc_type,
                            classifier_name=self.__class__.__name__
                        )
            
            logger.info(
                f"No good match found (best score: {best_score:.1f}), "
                "returning unknown"
            )
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            )
            
        except Exception as e:
            logger.error(f"Error during fuzzy classification: {str(e)}")
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            ) 