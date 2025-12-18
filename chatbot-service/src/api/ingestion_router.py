from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import logging
from pydantic import BaseModel

from src.services.embedding import EmbeddingService
from src.services.storage import StorageService
from src.db.qdrant_client import get_qdrant_client
from src.db.neon_client import get_db
from src.models.domain import TextbookContent, SectionMetadata

# Create the API router
router = APIRouter(prefix="/ingestion", tags=["ingestion"])

# Configure logging
logger = logging.getLogger(__name__)

# Request/Response models
class TextbookContentSchema(BaseModel):
    title: str
    content: str
    chapter: str = None
    section: str = None
    page_number: int = None

@router.post("/textbook-content")
async def add_textbook_content(content: TextbookContentSchema):
    """
    Add textbook content to the vector store
    """
    try:
        embedding_service = EmbeddingService()
        qdrant = get_qdrant_client()
        db = next(get_db())
        storage_service = StorageService(qdrant, db)
        
        # 1. Generate Embedding
        embedding = embedding_service.generate_embeddings([content.content])[0]
        
        # 2. Prepare Domain Object
        textbook_doc = TextbookContent(
            text=content.content,
            embedding=embedding,
            metadata=SectionMetadata(
                title=content.title,
                chapter=content.chapter,
                section=content.section,
                page_number=content.page_number
            )
        )
        
        # 3. Store
        storage_service.store_content([textbook_doc])
        
        return {"message": "Textbook content successfully added"}
        
    except Exception as e:
        logger.error(f"Error adding textbook content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and process it into the vector store
    """
    try:
        import PyPDF2
        import io
        
        if not file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read the PDF content
        pdf_data = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content found in PDF")
        
        embedding_service = EmbeddingService()
        qdrant = get_qdrant_client()
        db = next(get_db())
        storage_service = StorageService(qdrant, db)
        
        # Simplify chunking (for real RAG, use a better splitter)
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        embeddings = embedding_service.generate_embeddings(chunks)
        
        records = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            records.append(TextbookContent(
                text=chunk,
                embedding=emb,
                metadata=SectionMetadata(
                    title=f"{file.filename} - Part {i+1}",
                    chapter="Uploaded PDF",
                    section=file.filename,
                    page_number=0
                )
            ))
            
        storage_service.store_content(records)
        
        return {"message": f"Successfully processed PDF with {len(records)} chunks"}
        
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Ingestion API"}
