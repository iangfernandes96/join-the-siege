from pydantic import BaseModel, Field
from typing import List, Set


class ClassifierConfig(BaseModel):
    """Configuration for classifiers."""
    similarity_threshold: float = Field(default=80.0, description="Minimum similarity threshold for fuzzy matching")
    confidence_threshold: float = Field(default=0.4, description="Minimum confidence threshold for ML classifiers")
    max_features: int = Field(default=5000, description="Maximum number of features for TF-IDF")
    max_length: int = Field(default=512, description="Maximum sequence length for BERT")
    num_epochs: int = Field(default=5, description="Number of training epochs for BERT")


class DocumentPatterns(BaseModel):
    """Document classification patterns."""
    drivers_licence: List[str] = Field(
        default=[
            "drivers license",
            "driver's license",
            "drivers licence",
            "driver's licence",
            "driving license",
            "driving licence",
            "license",
            "licence",
            "permit",
            "id card",
            "identification",
            "driver id",
            "driver identification"
        ]
    )
    
    bank_statement: List[str] = Field(
        default=[
            "bank statement",
            "account statement",
            "banking statement",
            "statement of account",
            "account summary",
            "bank summary",
            "transaction history",
            "account history",
            "banking summary",
            "statement",
            "bank account",
            "account details",
            "banking details",
            "transaction summary"
        ]
    )
    
    invoice: List[str] = Field(
        default=[
            "invoice",
            "bill",
            "receipt",
            "payment",
            "charge",
            "fee",
            "cost",
            "amount due",
            "total amount",
            "price",
            "quote",
            "estimate",
            "statement",
            "debit note",
            "credit note",
            "order",
            "purchase order",
            "sales order"
        ]
    )


class AppConfig(BaseModel):
    """Main application configuration."""
    classifier: ClassifierConfig = Field(default_factory=ClassifierConfig)
    patterns: DocumentPatterns = Field(default_factory=DocumentPatterns)
    model_name: str = Field(default="distilbert-base-uncased")
    supported_file_types: List[str] = Field(
        default=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "image/jpeg",
            "image/png"
        ]
    )


ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'png', 'jpg', 'jpeg', 'xls',
                                'xlsx', 'doc', 'docx', 'csv', 'txt'}


config = AppConfig()