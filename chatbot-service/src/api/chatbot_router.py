from fastapi import APIRouter, Depends, HTTPException
from src.models.domain import UserQuery, ChatbotResponse
from src.services.embedding import EmbeddingService
from src.services.retrieval import RetrievalService
from src.services.generation import GenerationService
from src.db.qdrant_client import get_qdrant_client
from src.core.logging import logger

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/query", response_model=ChatbotResponse)
async def query_chatbot(query: UserQuery):
    """
    Process a user query:
    1. Embed query
    2. Retrieve relevant content
    3. Generate answer
    """
    try:
        # Initialize services (Dependency Injection could be improved here)
        embedding_service = EmbeddingService()
        qdrant_client = get_qdrant_client()
        retrieval_service = RetrievalService(qdrant_client)
        generation_service = GenerationService()
        
        # 1. Embed Query
        query_vector = embedding_service.generate_query_embedding(query.text)
        
        # 2. Retrieve Context
        context_items = retrieval_service.search_similar_content(query_vector)
        
        if not context_items:
            return ChatbotResponse(
                answer="I couldn't find any relevant information in the textbook to answer your question.",
                confidence_score=0.0,
                sources=[]
            )
            
        # 2.1 Calculate Aggregate Confidence
        # Use simple max score or average. In RAG, max hit score is often a good indicator of context relevance.
        confidence_score = max([item["score"] for item in context_items])
        logger.info(f"Query: '{query.text}' | Best Match Score: {confidence_score}")
        
        # 3. Generate Answer (Only if confidence is reasonable)
        if confidence_score < 0.15: # Threshold lowered from 0.25 to 0.15 to better capture relevant chapters
             return ChatbotResponse(
                answer="I'm not confident enough in the available textbook sections to answer that accurately. I found some related content but it might not be a direct match. Could you rephrase your question or ask about a specific chapter like Chapter 1, Robotics, or Control?",
                confidence_score=confidence_score,
                sources=[item["metadata"] for item in context_items]
            )

        answer = generation_service.generate_response(query.text, context_items)
        
        # Construct Response
        sources = []
        for item in context_items:
            meta = item["metadata"]
            # Combine chapter and section for the frontend 'title'
            meta.title = f"{meta.chapter} - {meta.section}"
            sources.append(meta)

        response = ChatbotResponse(
            answer=answer,
            confidence_score=confidence_score,
            sources=sources
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))