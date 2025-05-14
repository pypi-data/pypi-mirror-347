import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
from mkdocs_gemini_chat.server import app, ChatHandler
from mkdocs_gemini_chat.api import ChatResponse, ChatError

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_chat_handler():
    with patch('mkdocs_gemini_chat.server.chat_handler') as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
        yield

def test_chat_endpoint_success(client, mock_chat_handler):
    # Mock response
    mock_response = ChatResponse(
        text="Test response",
        success=True,
        metadata={'language': 'en', 'version': 'latest', 'has_context': False}
    )
    mock_chat_handler.handle_message.return_value = mock_response

    # Test request
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "test-api-key"},
        json={
            "message": "test message",
            "language": "en",
            "version": "latest"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["text"] == "Test response"
    assert data["metadata"]["language"] == "en"

def test_chat_endpoint_invalid_api_key(client):
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "invalid-key"},
        json={"message": "test"}
    )
    assert response.status_code == 401

def test_chat_endpoint_missing_api_key(client):
    response = client.post(
        "/api/chat",
        json={"message": "test"}
    )
    assert response.status_code == 422

def test_chat_endpoint_invalid_file_path(client, mock_chat_handler):
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "test-api-key"},
        json={
            "message": "test",
            "filePath": "../invalid/path"
        }
    )
    assert response.status_code == 400

def test_chat_endpoint_rate_limit(client, mock_chat_handler):
    # Make 11 requests (1 over limit)
    for i in range(11):
        response = client.post(
            "/api/chat",
            headers={"X-API-Key": "test-api-key"},
            json={"message": f"test {i}"}
        )
        if i == 10:  # Last request should be rate limited
            assert response.status_code == 429
        else:
            assert response.status_code == 200

def test_chat_endpoint_model_error(client, mock_chat_handler):
    mock_chat_handler.handle_message.side_effect = ChatError("Model error")
    
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "test-api-key"},
        json={"message": "test"}
    )
    assert response.status_code == 400
    assert "Model error" in response.json()["detail"] 