import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import os
from mkdocs_gemini_chat.server import app, ChatHandler
from mkdocs_gemini_chat.api import ChatResponse, ChatError

@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test-api-key',
        'TESTING': 'true'
    }):
        yield

@pytest.fixture
def client():
    # Create a mock chat handler with AsyncMock
    mock_handler = MagicMock()
    mock_handler.handle_message = AsyncMock(return_value=ChatResponse(
        text="Test response",
        success=True,
        metadata={'language': 'en', 'version': 'latest', 'has_context': False}
    ))
    # Set the mock handler in app state
    app.state.chat_handler = mock_handler
    client = TestClient(app)
    yield client
    # Cleanup
    app.state.chat_handler = None

def test_chat_endpoint_success(client):
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
        headers={},  # No API key header
        json={"message": "test"}
    )
    assert response.status_code == 401

def test_chat_endpoint_invalid_file_path(client):
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "test-api-key"},
        json={
            "message": "test",
            "filePath": "../invalid/path"
        }
    )
    assert response.status_code == 400

def test_chat_endpoint_model_error(client):
    # Set up error response with AsyncMock
    app.state.chat_handler.handle_message = AsyncMock(side_effect=ChatError("Model error"))
    
    response = client.post(
        "/api/chat",
        headers={"X-API-Key": "test-api-key"},
        json={"message": "test"}
    )
    assert response.status_code == 400
    assert "Model error" in response.json()["detail"] 