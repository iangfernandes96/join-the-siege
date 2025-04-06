from fastapi import UploadFile
from .base import BaseTextExtractor


class TextExtractor(BaseTextExtractor):
    """Extractor for plain text files."""

    async def _extract_text_handler(self, file: UploadFile) -> str:
        """
        Extract text from a plain text file.

        Args:
            file: The uploaded text file

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the text file cannot be processed
        """
        content = await file.read()
        return content.decode("utf-8").strip()
