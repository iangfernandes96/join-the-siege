from src.db.base import BaseDB
from src.models import ClassificationResponse


class InMemoryDB(BaseDB):
    def __init__(self):
        self.db = {}

    async def save_classification(self, classification: ClassificationResponse):
        self.db[classification.file_id] = classification

    async def get_classification(self, file_id: str) -> ClassificationResponse:
        return self.db.get(file_id)
