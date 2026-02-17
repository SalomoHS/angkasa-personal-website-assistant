from pydantic import BaseModel, Field
from typing import List, Literal

class ChatValidationResponse(BaseModel):
    response: str
    status: Literal["valid", "invalid"]

class ChatMessage(BaseModel):
    role: str 
    content: str

class ChatRequest(BaseModel):
    session_id: str
    query: str
    chat_history: List[ChatMessage] = Field(default_factory=list)

class ChatResponse(BaseModel):
    response: str

