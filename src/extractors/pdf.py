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

    async def _extract_text_handler(self, file: UploadFile) -> str:
        """
        Extract text from a PDF file.

        Args:
            file: The uploaded PDF file

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the PDF cannot be processed
        """
        content = await file.read()
        with BytesIO(content) as pdf_file:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception:
                        continue

                if not text.strip():
                    raise ValueError("No text could be extracted from the PDF")

                return text.strip()

