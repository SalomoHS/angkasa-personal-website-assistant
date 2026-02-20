from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.chat import ChatService

router = APIRouter()

def get_ai_service(request: Request):
    return ChatService(request)

@router.post("/chat")
async def chat(chat_request: ChatRequest, chat_service: ChatService = Depends(get_ai_service)):
    return StreamingResponse(
        chat_service.stream_message(session_id=chat_request.session_id, query=chat_request.query, chat_history=chat_request.chat_history),
        media_type="text/plain"
    )
