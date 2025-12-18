import logging
import sys
from src.core.config import get_settings

settings = get_settings()

def setup_logging():
    logging_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logger = logging.getLogger("ai_textbook_chatbot")
    logger.setLevel(logging_level)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging_level)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logging()
