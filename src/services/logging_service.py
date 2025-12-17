from typing import Optional
import logging
from datetime import datetime
from src.models.user_interaction_log import UserInteractionLog, UserInteractionLogCreate
from src.database.qdrant_client import QdrantClient

logger = logging.getLogger(__name__)

class LoggingService:
    """
    Service for logging user interactions and analytics
    """
    
    def __init__(self):
        self.qdrant_client = QdrantClient()
    
    def log_user_interaction(
        self, 
        user_id: Optional[str], 
        query_id: str, 
        response_id: str,
        rating: Optional[float] = None,
        feedback: Optional[str] = None
    ) -> str:
        """
        Log a user interaction for analytics purposes
        """
        try:
            # Create a unique ID for the interaction log
            import uuid
            log_id = str(uuid.uuid4())
            
            # Prepare the payload for Qdrant
            payload = {
                "id": log_id,
                "user_id": user_id,
                "query_id": query_id,
                "response_id": response_id,
                "rating": rating,
                "feedback": feedback,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Store in Qdrant
            self.qdrant_client.store_interaction_log(
                collection_name="user_interaction_logs",
                log_id=log_id,
                payload=payload
            )
            
            logger.info(f"Logged user interaction: {log_id}")
            return log_id
        except Exception as e:
            logger.error(f"Error logging user interaction: {str(e)}")
            raise
    
    def get_interaction_analytics(self, limit: int = 100) -> list:
        """
        Retrieve interaction analytics for monitoring and improvement
        """
        try:
            # Retrieve recent interactions
            interactions = self.qdrant_client.get_recent_interactions(
                collection_name="user_interaction_logs",
                limit=limit
            )
            
            return interactions
        except Exception as e:
            logger.error(f"Error retrieving interaction analytics: {str(e)}")
            raise