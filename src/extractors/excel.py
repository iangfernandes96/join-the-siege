import pandas as pd
from fastapi import UploadFile
from io import BytesIO
from .base import BaseTextExtractor


class ExcelExtractor(BaseTextExtractor):
    """Extractor for Excel files using pandas."""

    async def _extract_text_handler(self, file: UploadFile) -> str:
        """
        Extract text from an Excel file.

        Args:
            file: The uploaded Excel file

        Returns:
            str: The extracted text

        Raises:
            ValueError: If the Excel file cannot be processed
        """
        content = await file.read()
        with BytesIO(content) as excel_file:
            # Read all sheets
            excel = pd.ExcelFile(excel_file)
            text = []

            for sheet_name in excel.sheet_names:
                df = pd.read_excel(excel, sheet_name=sheet_name)
                # Convert DataFrame to string representation
                text.append(f"Sheet: {sheet_name}\n{df.to_string()}")

            return "\n\n".join(text)
