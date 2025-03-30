import pdfplumber
from fastapi import UploadFile
from io import BytesIO
import logging
from .base import BaseTextExtractor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractor(BaseTextExtractor):
    """Extractor for PDF files using pdfplumber."""
    
    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file: The uploaded PDF file
            
        Returns:
            str: The extracted text
            
        Raises:
            ValueError: If the PDF cannot be processed
        """
        try:
            content = await file.read()
            with BytesIO(content) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    text = ""
                    for page_num, page in enumerate(pdf.pages, 1):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                            logger.info(f"Successfully extracted text from page {page_num}")
                        except Exception as e:
                            logger.warning(f"Failed to extract text from page {page_num}: {str(e)}")
                            continue
                    
                    if not text.strip():
                        raise ValueError("No text could be extracted from the PDF")
                        
                    return text.strip()
        except Exception as e:
            logger.error(f"Failed to process PDF: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
        finally:
            await file.seek(0)