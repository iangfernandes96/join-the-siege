from fastapi import UploadFile
from .base import BaseTextExtractor


class TextExtractor(BaseTextExtractor):
    """Extractor for plain text files."""

    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from a plain text file.

        Args:
            file: The uploaded text file

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the text file cannot be processed
        """
        try:
            content = await file.read()
            return content.decode("utf-8").strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from text file: {str(e)}")
        finally:
            await file.seek(0)
