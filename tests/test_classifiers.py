import pytest
from fastapi import UploadFile
from io import BytesIO
from src.classifiers.fuzzy import FuzzyClassifier
from src.classifiers.regex import RegexClassifier
from src.classifiers.tfidf import TFIDFClassifier
from src.classifiers.composite import CompositeClassifier
from src.classifiers.filename import FilenameClassifier
from src.models import ClassifierResult


@pytest.fixture
def sample_file():
    """Create a sample file for testing."""
    content = (
        b"This is a sample bank statement with account details "
        b"and transaction history."
    )
    return UploadFile(file=BytesIO(content), filename="bank_statement.pdf")


@pytest.fixture
def sample_invoice_file():
    """Create a sample invoice file for testing."""
    content = b"INVOICE\nBill to: John Doe\nAmount due: $100\nPayment terms: Net 30"
    return UploadFile(file=BytesIO(content), filename="invoice.pdf")


@pytest.fixture
def sample_drivers_license_file():
    """Create a sample drivers license file for testing."""
    content = b"DRIVER'S LICENSE\nName: John Doe\nDL Number: 123456789"
    return UploadFile(file=BytesIO(content), filename="drivers_license.pdf")


@pytest.mark.asyncio
async def test_fuzzy_classifier(sample_file):
    """Test fuzzy classifier with a bank statement."""
    classifier = FuzzyClassifier()
    result = await classifier.classify(sample_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "bank_statement"
    assert result.classifier_name == "FuzzyClassifier"


@pytest.mark.asyncio
async def test_regex_classifier(sample_invoice_file):
    """Test regex classifier with an invoice."""
    classifier = RegexClassifier()
    result = await classifier.classify(sample_invoice_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "invoice"
    assert result.classifier_name == "RegexClassifier"


@pytest.mark.asyncio
async def test_tfidf_classifier(sample_drivers_license_file):
    """Test TF-IDF classifier with a drivers license."""
    classifier = TFIDFClassifier()
    result = await classifier.classify(sample_drivers_license_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "drivers_licence"
    assert result.classifier_name == "TFIDFClassifier"


@pytest.mark.asyncio
async def test_composite_classifier(sample_file):
    """Test composite classifier with multiple classifiers."""
    classifiers = [FuzzyClassifier(), RegexClassifier(), TFIDFClassifier()]
    classifier = CompositeClassifier(classifiers=classifiers)
    result = await classifier.classify(sample_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type in ["bank_statement", "invoice", "drivers_licence"]
    assert result.classifier_name in [c.__class__.__name__ for c in classifiers]


@pytest.mark.asyncio
async def test_filename_classifier(sample_file):
    """Test filename classifier with a bank statement filename."""
    classifier = FilenameClassifier()
    result = await classifier.classify(sample_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "bank_statement"
    assert result.classifier_name == "FilenameClassifier"


@pytest.mark.asyncio
async def test_classifier_no_file():
    """Test classifier behavior with no file."""
    classifier = FuzzyClassifier()
    result = await classifier.classify(None)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "unknown"
    assert result.classifier_name == "FuzzyClassifier"


@pytest.mark.asyncio
async def test_classifier_empty_file():
    """Test classifier behavior with empty file."""
    empty_file = UploadFile(file=BytesIO(b""), filename="empty.pdf")
    classifier = FuzzyClassifier()
    result = await classifier.classify(empty_file)
    assert isinstance(result, ClassifierResult)
    assert result.document_type == "unknown"
    assert result.classifier_name == "FuzzyClassifier"
