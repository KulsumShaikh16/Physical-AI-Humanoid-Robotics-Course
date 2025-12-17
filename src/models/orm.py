from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.db.neon_client import Base

class TextbookContentORM(Base):
    __tablename__ = "textbook_content"

    id = Column(String, primary_key=True, index=True) # UUID
    text = Column(Text, nullable=False)
    chapter = Column(String, nullable=False)
    section = Column(String, nullable=False)
    page_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
