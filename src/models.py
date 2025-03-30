from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import UploadFile


class ClassificationRequest(BaseModel):
    """Request model for file classification."""
    file: UploadFile = Field(..., description="The file to classify")


class ClassificationResponse(BaseModel):
    """Response model for file classification."""
    document_type: str = Field(..., description="The classified document type")


class ClassificationError(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")


class ClassifierStats(BaseModel):
    """Statistics for a classifier."""
    name: str = Field(..., description="Name of the classifier")
    success_rate: float = Field(..., description="Success rate of classifications")
    average_confidence: float = Field(..., description="Average confidence score")
    total_classifications: int = Field(..., description="Total number of classifications")


class SystemStats(BaseModel):
    """Overall system statistics."""
    classifiers: List[ClassifierStats] = Field(..., description="Stats for each classifier")
    total_requests: int = Field(..., description="Total number of classification requests")
    average_response_time: float = Field(..., description="Average response time in seconds") 