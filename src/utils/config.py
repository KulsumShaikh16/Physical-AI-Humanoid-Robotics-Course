import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """
    Configuration class to manage application settings
    """

    # API settings - either OpenAI or Google Gemini
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "localhost")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Application settings
    APP_TITLE: str = "AI Textbook RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A RAG chatbot for answering questions about physical AI and humanoid robotics textbooks"

    # Model settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    GENERATION_MODEL: str = os.getenv("GENERATION_MODEL", "gpt-3.5-turbo")

    # Vector database settings
    TEXT_CHUNK_SIZE: int = int(os.getenv("TEXT_CHUNK_SIZE", "1000"))
    TEXT_CHUNK_OVERLAP: int = int(os.getenv("TEXT_CHUNK_OVERLAP", "200"))

    # Retrieval settings
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))

    # Rate limiting (if implemented)
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # in seconds

    @classmethod
    def validate_config(cls):
        """
        Validate that required configurations are set
        """
        errors = []

        # Check if at least one API key is set
        if not cls.OPENAI_API_KEY and not cls.GEMINI_API_KEY:
            errors.append("Either OPENAI_API_KEY or GEMINI_API_KEY must be set")

        if not errors:
            return True, "Configuration is valid"
        else:
            return False, "; ".join(errors)