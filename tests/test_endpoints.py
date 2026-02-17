from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.api.v1.chat import get_ai_service

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

async def mock_stream_message(query, chat_history):
    yield "Hello"
    yield " world"

def test_chat_endpoint():
    # Create a mock service
    mock_service = MagicMock()
    # Configure the mock to return an async generator
    mock_service.stream_message = mock_stream_message

    # Override the dependency
    app.dependency_overrides[get_ai_service] = lambda: mock_service

    try:
        response = client.post(
            "/api/v1/chat",
            json={
                "query": "Hello",
                "chat_history": []
            }
        )
        
        assert response.status_code == 200
        # For streaming response, TestClient.post returns the concatenated content
        assert response.text == "Hello world"
    finally:
        # Clean up the override
        app.dependency_overrides = {}
