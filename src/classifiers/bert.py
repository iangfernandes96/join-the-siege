import logging
from fastapi import UploadFile
import torch
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)
from .base import BaseClassifier

# Set up logging
logger = logging.getLogger(__name__)


class BERTClassifier(BaseClassifier):
    """Classifier that uses DistilBERT for document classification."""
    
    def __init__(self):
        self.model_name = "distilbert-base-uncased"
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=3,  # drivers_licence, bank_statement, invoice
            id2label={
                0: "drivers_licence",
                1: "bank_statement",
                2: "invoice"
            },
            label2id={
                "drivers_licence": 0,
                "bank_statement": 1,
                "invoice": 2
            }
        )
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
            labels.extend([self.model.config.label2id[doc_type]] * len(examples))
        
        # Tokenize and prepare inputs
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Convert labels to tensor
        labels = torch.tensor(labels)
        
        # Train the model
        self.model.train()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=2e-5)
        
        for epoch in range(5):  # Increased number of epochs
            optimizer.zero_grad()
            outputs = self.model(**inputs, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            logger.info(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}")
        
        self.is_trained = True
        logger.info("BERT classifier trained successfully")
    
    async def classify(self, file: UploadFile) -> str:
        """
        Classify a file using DistilBERT.
        
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
            
            # Tokenize and prepare input
            inputs = self.tokenizer(
                text,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Get prediction
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
                prediction_id = torch.argmax(probabilities).item()
                confidence = probabilities[0][prediction_id].item()
            
            prediction = self.model.config.id2label[prediction_id]
            
            # Only return prediction if confidence is high enough
            if confidence >= 0.4:  # Increased confidence threshold
                logger.info(
                    f"Classified as '{prediction}' with confidence "
                    f"{confidence:.2f}"
                )
                return prediction
            
            logger.info(
                f"Low confidence prediction ({confidence:.2f}) for "
                f"'{prediction}', returning unknown"
            )
            return "unknown file"
            
        except Exception as e:
            logger.error(f"Error during BERT classification: {str(e)}")
            return "unknown file" 