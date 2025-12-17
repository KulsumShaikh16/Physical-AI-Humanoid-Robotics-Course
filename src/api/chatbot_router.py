from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
import logging
from pydantic import BaseModel

from src.services.retrieval_service import RetrievalService
from src.services.generation_service import GenerationService
from src.services.logging_service import LoggingService
from src.services.embedding_service import EmbeddingService
from src.database.vector_store import VectorStore
from src.models.user_query import UserQueryCreate
from src.models.textbook_content import TextbookContentCreate
from src.utils.config import Config

# Create the API router
router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Initialize services
retrieval_service = RetrievalService()
generation_service = GenerationService()
logging_service = LoggingService()
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    user_id: str = None

class QueryResponse(BaseModel):
    response: str
    confidence_score: float
    sources: List[Dict]

class ContentIngestionRequest(BaseModel):
    title: str
    content: str
    chapter: str = None
    section: str = None
    page_number: int = None

# Configure logging
logger = logging.getLogger(__name__)

@router.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    """
    Query the RAG chatbot and get a response
    """
    try:
        logger.info(f"Received query from user {request.user_id}: {request.query}")

        # Retrieve relevant content based on the query
        relevant_content = retrieval_service.retrieve_relevant_content(
            query=request.query,
            top_k=5
        )

        # Generate a response based on the retrieved content
        response_text = generation_service.generate_response(
            question=request.query,
            context=relevant_content
        )

        # Calculate confidence score based on the retrieved content
        confidence_score = generation_service.calculate_confidence(
            context=relevant_content,
            question=request.query
        )

        # Prepare sources for the response
        sources = [
            {
                "id": item["id"],
                "title": item["title"],
                "chapter": item["chapter"],
                "section": item["section"],
                "page_number": item["page_number"],
                "relevance_score": item["score"]
            }
            for item in relevant_content
        ]

        # Log the interaction
        try:
            query_for_log = f"Query: {request.query}"
            response_for_log = f"Response: {response_text}"
            logging_service.log_user_interaction(
                user_id=request.user_id,
                query_id="",  # In a real implementation, we'd create a proper query ID
                response_id="",  # In a real implementation, we'd create a proper response ID
            )
        except Exception as log_error:
            # Don't fail the query if logging fails
            logger.error(f"Error logging interaction: {str(log_error)}")

        return QueryResponse(
            response=response_text,
            confidence_score=confidence_score,
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/ingest")
async def ingest_content(content: ContentIngestionRequest):
    """
    Ingest textbook content into the vector store
    """
    try:
        # In a real implementation, we would process the content more thoroughly
        # For now, we'll add it directly to the vector store
        import uuid
        content_id = str(uuid.uuid4())

        # Create metadata dictionary
        metadata = {
            "title": content.title,
            "chapter": content.chapter,
            "section": content.section,
            "page_number": content.page_number,
            "created_at": "TODO",  # Would be set when stored
            "updated_at": "TODO"   # Would be set when stored
        }

        # Add to vector store
        success = vector_store.add_textbook_content(
            content_id=content_id,
            text=content.content,
            metadata=metadata
        )

        if success:
            logger.info(f"Successfully ingested content '{content.title}' with ID {content_id}")
            return {"message": "Content successfully ingested", "content_id": content_id}
        else:
            logger.error(f"Failed to ingest content '{content.title}'")
            raise HTTPException(status_code=500, detail="Failed to ingest content")
    except Exception as e:
        logger.error(f"Error ingesting content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error ingesting content: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Validate configuration
        is_valid, message = Config.validate_config()
        if not is_valid:
            logger.warning(f"Configuration validation failed: {message}")
            return {"status": "unhealthy", "details": message}

        # In a real implementation, we would check the status of external services
        # such as Qdrant and OpenAI API

        return {"status": "healthy", "service": "RAG Chatbot API"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


# Additional endpoints can be added as needed