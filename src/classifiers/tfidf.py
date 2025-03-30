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
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = MultinomialNB()
        self.is_trained = False
        
        # Training data for each document type
        self.training_data = {
            "drivers_licence": [
                "driver's license application form",
                "driver license renewal document",
                "driver's permit application",
                "driver identification card",
                "driver's license verification",
                "driver's license number",
                "driver's license expiration date",
                "driver's license photo",
                "driver's license address",
                "driver's license class",
                "driver's license renewal",
                "driver's license application",
                "driver's license test",
                "driver's license requirements",
                "driver's license office"
            ],
            "bank_statement": [
                "bank account statement",
                "monthly bank statement",
                "account transaction history",
                "banking statement summary",
                "account balance sheet",
                "bank statement period",
                "account statement date",
                "bank statement transactions",
                "account statement balance",
                "account statement details",
                "bank statement summary",
                "bank statement period",
                "bank statement balance",
                "bank statement transactions",
                "bank statement account"
            ],
            "invoice": [
                "invoice for services rendered",
                "payment invoice",
                "service invoice",
                "invoice number",
                "invoice date",
                "invoice amount due",
                "invoice payment terms",
                "invoice billing address",
                "invoice line items",
                "invoice total amount",
                "invoice payment",
                "invoice details",
                "invoice summary",
                "invoice total",
                "invoice items",
                "invoice for payment",
                "invoice to be paid",
                "invoice due date",
                "invoice amount",
                "invoice description",
                "invoice from",
                "invoice to",
                "invoice reference",
                "invoice status",
                "invoice type"
            ]
        }
    
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
    
    async def classify(self, file: UploadFile) -> ClassifierResult:
        """
        Classify a file using TF-IDF and Naïve Bayes.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            ClassifierResult: The classification result
        """
        try:
            # Train the classifier if not already trained
            if not self.is_trained:
                self.train()
            
            extractor = TextExtractorFactory.get_extractor(file)
            
            # Extract text from the file
            text = await extractor.extract_text(file)
            logger.info(f"Extracted text from file: {file.filename}")
            
            # Transform text to TF-IDF features
            X = self.vectorizer.transform([text])
            
            # Get prediction and probabilities
            prediction = self.classifier.predict(X)[0]
            probabilities = self.classifier.predict_proba(X)[0]
            confidence = np.max(probabilities)
            
            # Only return prediction if confidence is high enough
            if confidence >= config.classifier.confidence_threshold:
                logger.info(
                    f"Classified as '{prediction}' with confidence "
                    f"{confidence:.2f}"
                )
                return ClassifierResult(
                    document_type=prediction,
                    classifier_name=self.__class__.__name__
                )
            
            logger.info(
                f"Low confidence prediction ({confidence:.2f}) for "
                f"'{prediction}', returning unknown"
            )
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            )
            
        except Exception as e:
            logger.error(f"Error during TF-IDF classification: {str(e)}")
            return ClassifierResult(
                classifier_name=self.__class__.__name__
            ) 