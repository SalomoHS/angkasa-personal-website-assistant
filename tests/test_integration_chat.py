import requests
import pytest
import os

# Default to localhost:8000 if not specified
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:1234")

def test_chat_with_history_real_payload():
    """
    Test the chat endpoint with history.
    """
    url = f"{BASE_URL}/api/v1/chat"
    payload = {
        "session_id": "test-integration-session",
        "query": "What are your skills?",
        "chat_history": [
            {"role": "user", "content": "So, what can i help ?"},
        ]
    }
    
    print(f"Connecting to {url}...")
    try:
        # Enable streaming
        with requests.post(url, json=payload, stream=True) as response:
            assert response.status_code == 200
            print("Response stream started...")
            
            full_response = ""
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    print(f"Chunk received: {chunk}", end="", flush=True)
                    full_response += chunk
            
            print("\nStream finished.")
            assert len(full_response) > 0

    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to {url}. Is the server running? Please start it with 'uv run uvicorn app.main:app --reload'")

test_chat_with_history_real_payload()