from typing import List, Dict, Optional
import logging
from src.models.textbook_content import TextbookContent
from src.database.qdrant_client import QdrantClient
from src.services.embedding_service import EmbeddingService
import os

logger = logging.getLogger(__name__)

class RetrievalService:
    """
    Service for retrieving relevant textbook content based on user queries
    """
    
    def __init__(self):
        self.qdrant_client = QdrantClient()
        self.embedding_service = EmbeddingService()
        
    def retrieve_relevant_content(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve the most relevant textbook content based on a user query
        """
        try:
            # Create embedding for the query
            query_embedding = self.embedding_service.create_embeddings(query)
            
            # Search in Qdrant for similar content
            results = self.qdrant_client.search(
                collection_name="textbook_content",
                query_vector=query_embedding,
                limit=top_k
            )
            
            # Format the results
            relevant_content = []
            for result in results:
                content = {
                    "id": result.payload.get("id"),
                    "title": result.payload.get("title"),
                    "content": result.payload.get("content"),
                    "chapter": result.payload.get("chapter"),
                    "section": result.payload.get("section"),
                    "page_number": result.payload.get("page_number"),
                    "score": result.score
                }
                relevant_content.append(content)
                
            return relevant_content
        except Exception as e:
            logger.error(f"Error retrieving relevant content: {str(e)}")
            raise
    
    def retrieve_by_id(self, content_id: str) -> Optional[TextbookContent]:
        """
        Retrieve a specific piece of content by its ID
        """
        try:
            result = self.qdrant_client.retrieve_by_id(
                collection_name="textbook_content",
                content_id=content_id
            )
            
            if result:
                # Convert Qdrant result to TextbookContent model
                payload = result.payload
                return TextbookContent(
                    id=payload.get("id"),
                    title=payload.get("title"),
                    content=payload.get("content"),
                    chapter=payload.get("chapter"),
                    section=payload.get("section"),
                    page_number=payload.get("page_number"),
                    created_at=payload.get("created_at"),
                    updated_at=payload.get("updated_at")
                )
            return None
        except Exception as e:
            logger.error(f"Error retrieving content by ID: {str(e)}")
            raise