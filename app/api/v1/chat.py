from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.chat import ChatService

router = APIRouter()

def get_ai_service():
    return ChatService()

@router.post("/chat")
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_ai_service)):
    return StreamingResponse(
        chat_service.stream_message(query=request.query, chat_history=request.chat_history),
        media_type="text/plain"
    )
