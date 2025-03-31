from pydantic import BaseModel, Field
from fastapi import UploadFile
from typing import Optional


class ClassifierResult(BaseModel):
    """Result from a single classifier."""

    document_type: str = Field(
        default="unknown", description="The classified document type"
    )
    classifier_name: str = Field(
        ..., description="Name of the classifier that made the decision"
    )


class ClassificationRequest(BaseModel):
    """Request model for file classification."""

    file: UploadFile = Field(..., description="The file to classify")


class ClassificationResponse(ClassifierResult):
    """Response model for file classification."""

    pass


class ClassificationError(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
