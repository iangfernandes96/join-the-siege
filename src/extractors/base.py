from abc import ABC, abstractmethod
from fastapi import UploadFile


class BaseTextExtractor(ABC):
    """Base class for text extraction from different file types."""

    @abstractmethod
    async def _extract_text_handler(self, file: UploadFile) -> str:
        """
        Custom handler to be implemented by subclasses
        for text extraction from the given file.
        """
        pass

    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from the given file.

        Args:
            file: The uploaded file to extract text from

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the file cannot be processed
        """
        try:
            return await self._extract_text_handler(file)
        except Exception as e:
            raise ValueError(f"Error extracting text from file: {e}")
        finally:
            await file.seek(0)
