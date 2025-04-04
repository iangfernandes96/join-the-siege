import logging
from fastapi import UploadFile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from .base import BaseClassifier
from ..config import config
from ..models import ClassifierResult
from ..extractors.factory import TextExtractorFactory

# Set up logging
logger = logging.getLogger(__name__)


class TFIDFClassifier(BaseClassifier):
    """Classifier that uses TF-IDF and Naïve Bayes for
    document classification."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=config.classifier.max_features,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self.classifier = MultinomialNB()
        self.is_trained = False
        self.training_data = config.tfidf_training_data

    def train(self):
        """Train the classifier with the training data."""
        if self.is_trained:
            return

        # Prepare training data
        texts = []
        labels = []

        for doc_type, examples in self.training_data.items():
            texts.extend(examples)
            labels.extend([doc_type] * len(examples))

        # Transform text to TF-IDF features
        X = self.vectorizer.fit_transform(texts)

        # Train the classifier
        self.classifier.fit(X, labels)
        self.is_trained = True
        logger.info("TF-IDF classifier trained successfully")

    async def classify(self, filename: str, content: str) -> ClassifierResult:
        """
        Classify a file using TF-IDF and Naïve Bayes.

        Args:
            filename: The name of the file
            content: The text content of the file

        Returns:
            ClassifierResult: The classification result
        """
        try:
            # Train the classifier if not already trained
            if not self.is_trained:
                self.train()

            # Transform text to TF-IDF features

            # Transform text to TF-IDF features
            X = self.vectorizer.transform([content])

            # Get prediction and probabilities
            prediction = self.classifier.predict(X)[0]
            probabilities = self.classifier.predict_proba(X)[0]
            confidence = np.max(probabilities)

            # Only return prediction if confidence is high enough
            if confidence >= config.classifier.confidence_threshold:
                logger.info(
                    f"Classified as '{prediction}' with confidence " f"{confidence:.2f}"
                )
                return ClassifierResult(
                    document_type=prediction, classifier_name=self.__class__.__name__
                )

            logger.info(
                f"Low confidence prediction ({confidence:.2f}) for "
                f"'{prediction}', returning unknown"
            )
            return ClassifierResult(classifier_name=self.__class__.__name__)

        except Exception as e:
            logger.error(f"Error during TF-IDF classification: {str(e)}")
            return ClassifierResult(classifier_name=self.__class__.__name__)
