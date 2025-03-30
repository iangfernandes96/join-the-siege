import pytesseract
from PIL import Image
from fastapi import UploadFile
from io import BytesIO
from .base import BaseTextExtractor


class ImageExtractor(BaseTextExtractor):
    """Extractor for image files using pytesseract OCR."""
    
    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            file: The uploaded image file
            
        Returns:
            str: The extracted text
            
        Raises:
            ValueError: If the image cannot be processed
        """
        try:
            content = await file.read()
            with BytesIO(content) as image_file:
                image = Image.open(image_file)
                text = pytesseract.image_to_string(image)
                return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from image: {str(e)}")
        finally:
            await file.seek(0)  # Reset file pointer for potential reuse 