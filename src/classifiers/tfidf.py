from typing import Dict, List
import logging
from fastapi import UploadFile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from .base import BaseClassifier

# Set up logging
logger = logging.getLogger(__name__)


class TFIDFClassifier(BaseClassifier):
    """Classifier that uses TF-IDF and Naive Bayes for document classification."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
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
                "driver's license class"
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
                "bank statement details"
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
                "invoice total amount"
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
        y = np.array(labels)
        
        # Train the classifier
        self.classifier.fit(X, y)
        self.is_trained = True
        logger.info("TF-IDF classifier trained successfully")
    
    async def classify(self, file: UploadFile) -> str:
        """
        Classify a file using TF-IDF and Naive Bayes.
        
        Args:
            file: The uploaded file to classify
            
        Returns:
            str: The classification result
        """
        try:
            # Train the classifier if not already trained
            if not self.is_trained:
                self.train()
            
            # Get the appropriate extractor for the file type
            from ..extractors.factory import TextExtractorFactory
            extractor = TextExtractorFactory.get_extractor(file)
            
            # Extract text from the file
            text = await extractor.extract_text(file)
            logger.info(f"Extracted text from file: {file.filename}")
            
            # Transform the text using the trained vectorizer
            X = self.vectorizer.transform([text])
            
            # Get prediction and probability
            prediction = self.classifier.predict(X)[0]
            probabilities = self.classifier.predict_proba(X)[0]
            max_prob = np.max(probabilities)
            
            # Only return prediction if confidence is high enough
            if max_prob >= 0.3:  # Confidence threshold
                logger.info(
                    f"Classified as '{prediction}' with confidence "
                    f"{max_prob:.2f}"
                )
                return prediction
            
            logger.info(
                f"Low confidence prediction ({max_prob:.2f}) for "
                f"'{prediction}', returning unknown"
            )
            return "unknown file"
            
        except Exception as e:
            logger.error(f"Error during TF-IDF classification: {str(e)}")
            return "unknown file" 