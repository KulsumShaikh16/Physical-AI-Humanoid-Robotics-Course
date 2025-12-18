from typing import List
from src.services.embedding import EmbeddingService
from src.services.storage import StorageService
from src.models.domain import TextbookContent, SectionMetadata
from src.core.logging import logger

class IngestionService:
    def __init__(self, embedding_service: EmbeddingService, storage_service: StorageService):
        self.embedding_service = embedding_service
        self.storage_service = storage_service

    def ingest_content(self, text_chunks: List[TextbookContent]):
        """
        Orchestrates the ingestion process.
        Accepts a list of TextbookContent objects.
        """
        logger.info(f"Starting ingestion for {len(text_chunks)} chunks.")
        
        texts = [chunk.text for chunk in text_chunks]
        
        # Batch generation of embeddings
        embeddings = self.embedding_service.generate_embeddings(texts)
        
        for i, content in enumerate(text_chunks):
            content.embedding = embeddings[i]
            
        self.storage_service.store_content(text_chunks)
        logger.info("Ingestion complete.")
