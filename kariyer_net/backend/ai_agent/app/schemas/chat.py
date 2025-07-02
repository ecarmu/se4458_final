from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = None
    actions: Optional[List[dict]] = None 