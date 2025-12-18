from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TextbookContentBase(BaseModel):
    """Base model for textbook content"""
    title: str
    content: str
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None


class TextbookContentCreate(TextbookContentBase):
    """Model for creating new textbook content"""
    pass


class TextbookContentUpdate(BaseModel):
    """Model for updating textbook content"""
    title: Optional[str] = None
    content: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None


class TextbookContent(TextbookContentBase):
    """Model for textbook content with ID and metadata"""
    id: str
    embedding: Optional[List[float]] = None  # Optional, as embedding might be generated later
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True