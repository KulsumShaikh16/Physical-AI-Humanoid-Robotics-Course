from fastapi import APIRouter, Depends, HTTPException
import time
import sys
from src.models.domain import UserQuery, ChatbotResponse
from src.services.embedding import EmbeddingService
from src.services.retrieval import RetrievalService
from src.services.generation import GenerationService
from src.db.qdrant_client import get_qdrant_client
from src.core.logging import logger

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

from fastapi.responses import StreamingResponse
import json

@router.post("/query")
async def query_chatbot_stream(query: UserQuery):
    """
    Process a user query and stream the response:
    1. Embed query
    2. Retrieve relevant content
    3. Generate answer stream
    """
    try:
        # Initialize services
        embedding_service = EmbeddingService()
        qdrant_client = get_qdrant_client()
        retrieval_service = RetrievalService(qdrant_client)
        generation_service = GenerationService()
        
        # 1. Embed Query
        start_time = time.time()
        query_vector = embedding_service.generate_query_embedding(query.text)
        embed_time = time.time() - start_time

        
        # 2. Retrieve Context
        start_time = time.time()
        context_items = retrieval_service.search_similar_content(query_vector)
        retrieve_time = time.time() - start_time

        
        sources = []
        confidence_score = 0.0
        
        if context_items:
             confidence_score = max([item["score"] for item in context_items])
             for item in context_items:
                meta = item["metadata"]
                # Create a dict from the Pydantic model if needed, or use .dict()/.model_dump()
                # Assuming meta is a Pydantic model or similar object
                source_dict = {
                    "title": f"{meta.chapter} - {meta.section}",
                    "chapter": meta.chapter,
                    "section": meta.section,
                    "page_number": meta.page_number
                }
                sources.append(source_dict)

        # Generator for streaming response
        def response_generator():
            # 1. Send Metadata Chunk
            metadata = {
                "type": "metadata",
                "confidence_score": confidence_score,
                "sources": sources
            }
            yield json.dumps(metadata) + "\n"
            
            # Handle low confidence / no context
            if not context_items:
                 yield json.dumps({"type": "content", "chunk": "I couldn't find any relevant information in the textbook to answer your question."}) + "\n"
                 return

            if confidence_score < 0.15:
                yield json.dumps({"type": "content", "chunk": "I'm not confident enough in the available textbook sections to answer that accurately. I found some related content but it might not be a direct match. Could you rephrase your question or ask about a specific chapter like Chapter 1, Robotics, or Control?"}) + "\n"
                return

            # 2. Stream Generation chunks
            start_gen = time.time()
            for chunk in generation_service.generate_response_stream(query.text, context_items):
                yield json.dumps({"type": "content", "chunk": chunk}) + "\n"
            
            gen_time = time.time() - start_gen


        return StreamingResponse(response_generator(), media_type="application/x-ndjson")
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))