from abc import ABC, abstractmethod
from src.models import ClassificationResponse


class BaseDB(ABC):
    @abstractmethod
    async def save_classification(self, classification: ClassificationResponse):
        pass

    @abstractmethod
    async def get_classification(self, file_id: str) -> ClassificationResponse:
        pass
