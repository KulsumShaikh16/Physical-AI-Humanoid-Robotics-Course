import cohere
from typing import List
from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()

class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(settings.COHERE_API_KEY)
        self.model = "embed-english-v3.0"  # Or use settings.EMBEDDING_MODEL if applicable
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks using Cohere.
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def generate_query_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single query string.
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise
