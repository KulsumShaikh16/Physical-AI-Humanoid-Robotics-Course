from typing import List
from qdrant_client import QdrantClient
from src.core.config import get_settings
from src.models.domain import SectionMetadata
from src.core.logging import logger

settings = get_settings()

class RetrievalService:
    def __init__(self, qdrant: QdrantClient):
        self.qdrant = qdrant
        self.collection_name = "textbook_embeddings_v3"

    def search_similar_content(self, query_vector: List[float], limit: int = 3) -> List[dict]:
        """
        Search Qdrant for similar content using the query vector.
        Returns a list of dicts with text, metadata, and normalized score.
        """
        try:
            results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                with_payload=True,
                limit=limit
            )
            
            retrieved_items = []
            for hit in results:
                payload = hit.payload
                # Qdrant cosine similarity is -1 to 1, but for RAG it's usually 0 to 1+.
                # We'll treat hit.score as the confidence basis.
                retrieved_items.append({
                    "text": payload.get("text_preview", ""),
                    "score": float(hit.score),
                    "metadata": SectionMetadata(
                        title=payload.get("title"),
                        chapter=payload.get("chapter"),
                        section=payload.get("section"),
                        page_number=payload.get("page_number")
                    )
                })
            
            return retrieved_items
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
