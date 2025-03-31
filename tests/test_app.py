import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from src.app import app, allowed_file
from src.models import ClassifierResult


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("file.pdf", True),
        ("file.png", True),
        ("file.jpg", True),
        ("file.txt", True),
        ("file", False),
    ],
)
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected


def test_no_file_in_request(client):
    response = client.post("/classify_file", files={})
    assert response.status_code == 400
    assert "No file or filename provided" in response.json()["detail"]


def test_no_selected_file(client):
    response = client.post("/classify_file", files={"file": ("", BytesIO(b""))})
    assert response.status_code == 422  # FastAPI validation error
    assert "value_error" in response.json()["detail"][0]["type"]


def test_success(client, mocker):
    mock_result = ClassifierResult(
        document_type="test_class", classifier_name="TestClassifier"
    )
    mocker.patch("src.app.classify_file", return_value=mock_result)

    response = client.post(
        "/classify_file", files={"file": ("file.pdf", BytesIO(b"dummy content"))}
    )
    assert response.status_code == 200
    assert response.json() == {
        "document_type": "test_class",
        "classifier_name": "TestClassifier",
    }
