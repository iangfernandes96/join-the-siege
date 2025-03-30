from pydantic import BaseModel, Field
from typing import List, Set, Dict


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


class RegexPatterns(BaseModel):
    """Regex patterns for document classification."""
    drivers_licence: List[str] = Field(
        default=[
                r"drivers?\s*licen[sc]e",
                r"dl\s*number",
                r"driver\s*id",
                r"drivers?\s*permit"
            ]
        )
    
    bank_statement: List[str] = Field(
        default=[
                r"bank\s*statement",
                r"account\s*statement",
                r"transaction\s*history",
                r"account\s*summary",
                r"balance\s*sheet",
                r"account\s*balance",
                r"statement\s*period"
            ]
    )

    invoice: List[str] = Field(
        default=[
                r"invoice",
                r"bill\s*to",
                r"amount\s*due",
                r"payment\s*terms",
                r"invoice\s*number",
                r"invoice\s*date"
            ]
    )


class AppConfig(BaseModel):
    """Main application configuration."""
    classifier: ClassifierConfig = Field(default_factory=ClassifierConfig)
    patterns: DocumentPatterns = Field(default_factory=DocumentPatterns)
    regex_patterns: RegexPatterns = Field(default_factory=RegexPatterns)
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
    mime_to_extension: Dict[str, str] = Field(
        default={
                'application/pdf': 'pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                'application/msword': 'doc',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
                'application/vnd.ms-excel': 'xls',
                'text/plain': 'txt',
                'text/csv': 'csv'
            }
    )


ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'png', 'jpg', 'jpeg', 'xls',
                                'xlsx', 'doc', 'docx', 'csv', 'txt'}


config = AppConfig()