from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatbotResponseBase(BaseModel):
    """Base model for chatbot responses"""
    query_id: str
    response_text: str
    confidence_score: float
    sources: Optional[List[dict]] = []


class ChatbotResponseCreate(ChatbotResponseBase):
    """Model for creating new chatbot responses"""
    pass


class ChatbotResponseUpdate(BaseModel):
    """Model for updating chatbot responses"""
    response_text: Optional[str] = None
    confidence_score: Optional[float] = None
    sources: Optional[List[dict]] = None


class ChatbotResponse(ChatbotResponseBase):
    """Model for chatbot responses with ID and metadata"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True