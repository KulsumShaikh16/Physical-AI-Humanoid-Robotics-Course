from typing import List, Dict, Optional
import logging
from src.database.qdrant_client import QdrantClient
from src.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class VectorStore:
    """
    High-level interface for vector storage operations
    """
    
    def __init__(self):
        self.qdrant_client = QdrantClient()
        self.embedding_service = EmbeddingService()
    
    def add_textbook_content(self, content_id: str, text: str, metadata: Dict):
        """
        Add textbook content to the vector store
        """
        try:
            # Create embedding for the text
            embedding = self.embedding_service.create_embeddings(text)
            
            # Add metadata to the payload
            payload = {
                "id": content_id,
                "content": text,
                **metadata  # Include any additional metadata
            }
            
            # Store in Qdrant
            self.qdrant_client.store_textbook_content(
                collection_name="textbook_content",
                content_id=content_id,
                embedding=embedding,
                payload=payload
            )
            
            logger.info(f"Added textbook content '{content_id}' to vector store")
            return True
        except Exception as e:
            logger.error(f"Error adding textbook content: {str(e)}")
            return False
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar content to the query
        """
        try:
            # Get embedding for the query
            query_embedding = self.embedding_service.create_embeddings(query)
            
            # Search in Qdrant
            results = self.qdrant_client.search(
                collection_name="textbook_content",
                query_vector=query_embedding,
                limit=top_k
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result.payload.get("id"),
                    "content": result.payload.get("content"),
                    "metadata": {k: v for k, v in result.payload.items() if k not in ["id", "content"]},
                    "similarity_score": result.score
                }
                formatted_results.append(formatted_result)
            
            logger.info(f"Search completed, found {len(formatted_results)} similar results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching for similar content: {str(e)}")
            raise
    
    def get_content_by_id(self, content_id: str) -> Optional[Dict]:
        """
        Retrieve specific content by ID
        """
        try:
            result = self.qdrant_client.retrieve_by_id(
                collection_name="textbook_content",
                content_id=content_id
            )
            
            if result:
                return {
                    "id": result.payload.get("id"),
                    "content": result.payload.get("content"),
                    "metadata": {k: v for k, v in result.payload.items() if k not in ["id", "content"]}
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving content by ID: {str(e)}")
            raise