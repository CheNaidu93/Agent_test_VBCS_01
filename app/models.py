from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique user or session identifier")
    message: str = Field(..., description="Message payload from user")

class ChatResponse(BaseModel):
    user_id: str
    response: str
    history_length: int
