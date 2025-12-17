from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserQueryBase(BaseModel):
    """Base model for user queries"""
    query_text: str
    user_id: Optional[str] = None


class UserQueryCreate(UserQueryBase):
    """Model for creating new user queries"""
    pass


class UserQueryUpdate(BaseModel):
    """Model for updating user queries"""
    query_text: Optional[str] = None
    user_id: Optional[str] = None


class UserQuery(UserQueryBase):
    """Model for user queries with ID and metadata"""
    id: str
    created_at: datetime
    processed: bool = False

    class Config:
        from_attributes = True