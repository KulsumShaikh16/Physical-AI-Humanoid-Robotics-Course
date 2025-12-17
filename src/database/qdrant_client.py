import logging
from typing import List, Optional, Dict
from qdrant_client import QdrantClient as QdrantBaseClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class QdrantClient:
    """
    Client for interacting with Qdrant vector database
    """
    
    def __init__(self):
        # Initialize Qdrant client - if no URL is provided, it will connect to local instance
        qdrant_url = os.getenv("QDRANT_URL", "localhost")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if qdrant_api_key:
            self.client = QdrantBaseClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                prefer_grpc=True
            )
        else:
            self.client = QdrantBaseClient(host=qdrant_url, prefer_grpc=True)
    
    def create_collection(self, collection_name: str, vector_size: int = 1536):
        """
        Create a collection in Qdrant for storing embeddings
        Default vector_size of 1536 is for OpenAI's text-embedding-ada-002
        """
        try:
            # Check if collection already exists
            try:
                self.client.get_collection(collection_name)
                logger.info(f"Collection '{collection_name}' already exists")
                return
            except:
                # Collection doesn't exist, create it
                pass
            
            # Create the collection
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            
            logger.info(f"Created collection '{collection_name}' with vector size {vector_size}")
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def store_textbook_content(self, collection_name: str, content_id: str, embedding: List[float], payload: Dict):
        """
        Store textbook content with its embedding in Qdrant
        """
        try:
            # Ensure the collection exists
            self.create_collection(collection_name)
            
            # Prepare the point to store
            points = [PointStruct(
                id=content_id,
                vector=embedding,
                payload=payload
            )]
            
            # Upload the point to Qdrant
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            
            logger.info(f"Stored content '{content_id}' in collection '{collection_name}'")
        except Exception as e:
            logger.error(f"Error storing textbook content: {str(e)}")
            raise
    
    def search(self, collection_name: str, query_vector: List[float], limit: int = 5):
        """
        Search for similar content in the collection
        """
        try:
            # Perform the search
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            logger.info(f"Search completed in collection '{collection_name}', found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            raise
    
    def retrieve_by_id(self, collection_name: str, content_id: str):
        """
        Retrieve a specific piece of content by its ID
        """
        try:
            # Retrieve the specific point
            results = self.client.retrieve(
                collection_name=collection_name,
                ids=[content_id]
            )
            
            if results:
                logger.info(f"Retrieved content '{content_id}' from collection '{collection_name}'")
                return results[0]  # Return the first (and should be only) result
            else:
                logger.warning(f"No content found with ID '{content_id}' in collection '{collection_name}'")
                return None
        except Exception as e:
            logger.error(f"Error retrieving content by ID: {str(e)}")
            raise
    
    def store_interaction_log(self, collection_name: str, log_id: str, payload: Dict):
        """
        Store user interaction logs in Qdrant
        """
        try:
            # Ensure the collection exists
            self.create_collection(collection_name, vector_size=384)  # Smaller vector size for logs
            
            # For interaction logs, we'll create a simple embedding based on the query/response
            # In a real implementation, you might not need vectors for logs
            from langchain.embeddings import OpenAIEmbeddings
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            text_to_embed = f"{payload.get('query_id', '')} {payload.get('response_id', '')}"
            embedding = embeddings.embed_query(text_to_embed)
            
            # Prepare the point to store
            points = [PointStruct(
                id=log_id,
                vector=embedding,
                payload=payload
            )]
            
            # Upload the point to Qdrant
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            
            logger.info(f"Stored interaction log '{log_id}' in collection '{collection_name}'")
        except Exception as e:
            logger.error(f"Error storing interaction log: {str(e)}")
            raise
    
    def get_recent_interactions(self, collection_name: str, limit: int = 100):
        """
        Retrieve recent interaction logs from Qdrant
        """
        try:
            # For retrieving all recent points, we can use scroll
            results, _ = self.client.scroll(
                collection_name=collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            
            logger.info(f"Retrieved {len(results)} recent interactions from collection '{collection_name}'")
            return [result.payload for result in results]
        except Exception as e:
            logger.error(f"Error retrieving interaction logs: {str(e)}")
            raise