from docx import Document
from fastapi import UploadFile
from io import BytesIO
from .base import BaseTextExtractor


class DocxExtractor(BaseTextExtractor):
    """Extractor for Word documents using python-docx."""

    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from a Word document.

        Args:
            file: The uploaded Word document

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the document cannot be processed
        """
        try:
            content = await file.read()
            with BytesIO(content) as docx_file:
                doc = Document(docx_file)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from Word document: {str(e)}")
        finally:
            await file.seek(0)
