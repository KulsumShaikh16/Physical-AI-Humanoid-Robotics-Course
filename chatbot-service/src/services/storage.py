import uuid
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sqlalchemy.orm import Session
from src.core.config import get_settings
from src.models.domain import TextbookContent
from src.models.orm import TextbookContentORM
from src.core.logging import logger

settings = get_settings()

class StorageService:
    def __init__(self, qdrant: QdrantClient, db: Session):
        self.qdrant = qdrant
        self.db = db
        self.collection_name = "textbook_embeddings_v3" # Incremented version to ensure a clean reset with titles
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.qdrant.get_collection(self.collection_name)
        except Exception:
            logger.info(f"Collection {self.collection_name} not found. Creating...")
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )

    def store_content(self, contents: List[TextbookContent]):
        """
        Store content in both Neon Postgres (metadata/text) and Qdrant (vectors).
        """
        try:
            points = []
            orm_objects = []

            for content in contents:
                # Generate ID if not present
                doc_id = content.id or str(uuid.uuid4())
                
                # Prepare Qdrant point
                if content.embedding:
                    points.append(PointStruct(
                        id=str(uuid.uuid4()), # Vector ID can be distinct or same. Using random UUID for vector point
                        vector=content.embedding,
                        payload={
                            "content_id": doc_id,
                            "title": content.metadata.title,
                            "chapter": content.metadata.chapter,
                            "section": content.metadata.section,
                            "page_number": content.metadata.page_number,
                            "text_preview": content.text[:200]
                        }
                    ))

                # Prepare Neon ORM object
                orm_objects.append(TextbookContentORM(
                    id=doc_id,
                    text=content.text,
                    chapter=content.metadata.chapter,
                    section=content.metadata.section,
                    page_number=content.metadata.page_number
                ))

            # upsert to Qdrant
            if points:
                self.qdrant.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
            
            # upsert/insert to Neon
            self.db.bulk_save_objects(orm_objects)
            self.db.commit()
            
            logger.info(f"Successfully stored {len(contents)} chunks.")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to store content: {e}")
            raise
