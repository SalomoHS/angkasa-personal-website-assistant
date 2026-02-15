from fastapi import APIRouter, Request, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter()

def get_ai_service():
    return ChatService()

router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_ai_service)):
    return await chat_service.send_message(request.query, request.chat_history)
