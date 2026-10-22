from typing import Optional
from pydantic import BaseModel, Field


class ChatContext(BaseModel):
    application: str = "Oracle Fusion"
    page_type: str = "GENERAL"
    record_id: Optional[str] = None


class ChatRequest(BaseModel):
    # Keep these fields so the existing HTML chatbot
    # continues to work without changes.
    user_id: str = Field(..., description="Chat session identifier")
    message: str = Field(..., min_length=1)

    # New optional field for Fusion page context.
    context: Optional[ChatContext] = None


class ChatResponse(BaseModel):
    user_id: str
    response: str
    history_length: int

#from pydantic import BaseModel, Field

#class ChatRequest(BaseModel):
   # user_id: str = Field(..., description="Unique user or session identifier")
   # message: str = Field(..., description="Message payload from user")

#class ChatResponse(BaseModel):
  #  user_id: str
  #  response: str
    #history_length: int
