from fastapi import UploadFile
from .extractors.factory import TextExtractorFactory
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def classify_file(file: UploadFile) -> str:
    """
    Classify a file based on its content and metadata.
    
    Args:
        file: The uploaded file to classify
        
    Returns:
        str: The classification result
    """
    try:
        # Get the appropriate extractor for the file type
        extractor = TextExtractorFactory.get_extractor(file)
        
        # Extract text from the file
        text = await extractor.extract_text(file)
        logger.info(f"Extracted text from file: {file.filename} {text[:100]}")
        
        # Convert text to lowercase for case-insensitive matching
        text = text.lower()
        
        # Define classification patterns
        patterns = {
            "drivers_licence": [
                r"drivers?\s*licen[sc]e",
                r"dl\s*number",
                r"driver\s*id",
                r"drivers?\s*permit"
            ],
            "bank_statement": [
                r"bank\s*statement",
                r"account\s*statement",
                r"transaction\s*history",
                r"account\s*summary",
                r"balance\s*sheet",
                r"account\s*balance",
                r"statement\s*period"
            ],
            "invoice": [
                r"invoice",
                r"bill\s*to",
                r"amount\s*due",
                r"payment\s*terms",
                r"invoice\s*number",
                r"invoice\s*date"
            ]
        }
        
        # Check for patterns in the text
        for doc_type, doc_patterns in patterns.items():
            for pattern in doc_patterns:
                if re.search(pattern, text):
                    logger.info(f"Found pattern '{pattern}' for document type '{doc_type}'")
                    return doc_type
        
        # If no patterns found, try filename-based classification
        filename = file.filename.lower()
        logger.info("No content patterns found, falling back to filename analysis")
        
        if any(term in filename for term in ["drivers_license", "drivers_licence", "dl"]):
            return "drivers_licence"
            
        if any(term in filename for term in ["bank_statement", "account_statement", "statement"]):
            return "bank_statement"
            
        if "invoice" in filename:
            return "invoice"
        
        logger.warning(f"Could not classify file: {file.filename}")
        return "unknown file"
        
    except ValueError as e:
        logger.error(f"Error during classification: {str(e)}")
        # If text extraction fails, fall back to filename-based classification
        filename = file.filename.lower()
        
        if any(term in filename for term in ["drivers_license", "drivers_licence", "dl"]):
            return "drivers_licence"
            
        if any(term in filename for term in ["bank_statement", "account_statement", "statement"]):
            return "bank_statement"
            
        if "invoice" in filename:
            return "invoice"
        
        logger.warning(f"Could not classify file using filename: {file.filename}")
        return "unknown file"

