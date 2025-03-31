from pydantic import BaseModel, Field
from typing import List, Dict

# Maximum file size in MB
MAX_FILE_SIZE_MB = 10

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "jpg",
    "jpeg",
    "png",
    "csv",
    "txt",
}


class ClassifierConfig(BaseModel):
    """Configuration for classifiers."""

    similarity_threshold: float = Field(
        default=80.0, description="Minimum similarity threshold for fuzzy matching"
    )
    confidence_threshold: float = Field(
        default=0.65, description="Minimum confidence threshold for ML classifiers"
    )
    max_features: int = Field(
        default=5000, description="Maximum number of features for TF-IDF"
    )


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
            "driver identification",
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
            "transaction summary",
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
            "sales order",
        ]
    )


class RegexPatterns(BaseModel):
    """Regex patterns for document classification."""

    drivers_licence: List[str] = Field(
        default=[
            r"drivers?\s*licen[sc]e",
            r"dl\s*number",
            r"driver\s*id",
            r"drivers?\s*permit",
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
            r"statement\s*period",
        ]
    )

    invoice: List[str] = Field(
        default=[
            r"invoice",
            r"bill\s*to",
            r"amount\s*due",
            r"payment\s*terms",
            r"invoice\s*number",
            r"invoice\s*date",
        ]
    )


default_tf_idf_training_data: Dict[str, List[str]] = {
    "drivers_licence": [
        "driver's license application form",
        "driver license renewal document",
        "driver's permit application",
        "driver identification card",
        "driver's license verification",
        "driver's license number",
        "driver's license expiration date",
        "driver's license photo",
        "driver's license address",
        "driver's license class",
        "driver's license renewal",
        "driver's license application",
        "driver's license test",
        "driver's license requirements",
        "driver's license office",
    ],
    "bank_statement": [
        "bank account statement",
        "monthly bank statement",
        "account transaction history",
        "banking statement summary",
        "account balance sheet",
        "bank statement period",
        "account statement date",
        "bank statement transactions",
        "account statement balance",
        "account statement details",
        "bank statement summary",
        "bank statement period",
        "bank statement balance",
        "bank statement transactions",
        "bank statement account",
    ],
    "invoice": [
        "invoice for services rendered",
        "payment invoice",
        "service invoice",
        "invoice number",
        "invoice date",
        "invoice amount due",
        "invoice payment terms",
        "invoice billing address",
        "invoice line items",
        "invoice total amount",
        "invoice payment",
        "invoice details",
        "invoice summary",
        "invoice total",
        "invoice items",
        "invoice for payment",
        "invoice to be paid",
        "invoice due date",
        "invoice amount",
        "invoice description",
        "invoice from",
        "invoice to",
        "invoice reference",
        "invoice status",
        "invoice type",
    ],
}


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
            "image/png",
        ]
    )
    mime_to_extension: Dict[str, str] = Field(
        default={
            "application/pdf": "pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "application/vnd.ms-excel": "xls",
            "text/plain": "txt",
            "text/csv": "csv",
        }
    )
    tfidf_training_data: Dict[str, List[str]] = Field(
        default=default_tf_idf_training_data, description="Training data for TF-IDF"
    )


config = AppConfig()
