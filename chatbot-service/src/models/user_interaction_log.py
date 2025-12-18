from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserInteractionLogBase(BaseModel):
    """Base model for user interaction logs"""
    user_id: Optional[str] = None
    query_id: str
    response_id: str
    rating: Optional[float] = None  # Rating from 1-5 or None if not rated
    feedback: Optional[str] = None


class UserInteractionLogCreate(UserInteractionLogBase):
    """Model for creating new user interaction logs"""
    pass


class UserInteractionLogUpdate(BaseModel):
    """Model for updating user interaction logs"""
    rating: Optional[float] = None
    feedback: Optional[str] = None


class UserInteractionLog(UserInteractionLogBase):
    """Model for user interaction logs with ID and metadata"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True