from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Role = Literal["system", "user", "assistant"]

class ChatMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1)

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    stream: bool = False

class ChatResponse(BaseModel):
    model: str 
    reply: str
    