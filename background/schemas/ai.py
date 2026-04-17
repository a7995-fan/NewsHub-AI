from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    conversation_id: str = Field(None, description="会话ID，用于保持上下文")

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI回复消息")
    conversation_id: str = Field(..., description="会话ID")
