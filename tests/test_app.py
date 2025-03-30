from io import BytesIO
from fastapi.testclient import TestClient
import pytest
from src.app import app, allowed_file


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected


def test_no_file_in_request(client):
    response = client.post('/classify_file', files={})
    assert response.status_code == 400
    assert response.json()["detail"] == "No file provided"


def test_no_selected_file(client):
    response = client.post('/classify_file', files={"file": ("", BytesIO(b""))})
    assert response.status_code == 400
    assert response.json()["detail"] == "No filename provided"


def test_success(client, mocker):
    mocker.patch('src.app.classify_file', return_value='test_class')

    response = client.post(
        '/classify_file',
        files={"file": ("file.pdf", BytesIO(b"dummy content"))}
    )
    assert response.status_code == 200
    assert response.json() == {"file_class": "test_class"}