from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Domain Models

class SectionMetadata(BaseModel):
    title: Optional[str] = None
    chapter: str
    section: str
    page_number: int

class TextbookContent(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: SectionMetadata
    embedding: Optional[List[float]] = None

class UserQuery(BaseModel):
    text: str
    timestamp: datetime = datetime.now()

class ChatbotResponse(BaseModel):
    answer: str
    confidence_score: float
    sources: List[SectionMetadata]
