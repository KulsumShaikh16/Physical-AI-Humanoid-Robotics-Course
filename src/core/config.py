from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "AI Textbook RAG Chatbot"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API Keys & Secrets
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    COHERE_API_KEY: str
    HF_TOKEN: Optional[str] = None
    
    # Database Config
    NEON_DATABASE_URL: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    
    # Model Config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2" # Fallback or specific model
    GENERATION_MODEL: str = "gemini-pro"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
