from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import logging
from pydantic import BaseModel

from src.services.embedding_service import EmbeddingService
from src.database.vector_store import VectorStore
from src.utils.config import Config

# Create the API router
router = APIRouter(prefix="/ingestion", tags=["ingestion"])

# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Request/Response models
class TextbookContent(BaseModel):
    title: str
    content: str
    chapter: str = None
    section: str = None
    page_number: int = None

# Configure logging
logger = logging.getLogger(__name__)

@router.post("/textbook-content")
async def add_textbook_content(content: TextbookContent):
    """
    Add textbook content to the vector store
    """
    try:
        import uuid
        
        content_id = str(uuid.uuid4())
        
        # Create metadata dictionary
        metadata = {
            "title": content.title,
            "chapter": content.chapter,
            "section": content.section,
            "page_number": content.page_number,
        }
        
        # Add to vector store
        success = vector_store.add_textbook_content(
            content_id=content_id,
            text=content.content,
            metadata=metadata
        )
        
        if success:
            logger.info(f"Successfully added textbook content '{content.title}' with ID {content_id}")
            return {
                "message": "Textbook content successfully added", 
                "content_id": content_id
            }
        else:
            logger.error(f"Failed to add textbook content '{content.title}'")
            raise HTTPException(status_code=500, detail="Failed to add textbook content")
    except Exception as e:
        logger.error(f"Error adding textbook content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding textbook content: {str(e)}")


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and process it into the vector store
    """
    try:
        import uuid
        from PyPDF2 import PdfReader
        
        # Check file type
        if not file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read the PDF content
        pdf_reader = PdfReader(file.file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()
        
        if not content.strip():
            raise HTTPException(status_code=400, detail="No text content found in PDF")
        
        # Create a content ID
        content_id = str(uuid.uuid4())
        
        # Add to vector store
        success = vector_store.add_textbook_content(
            content_id=content_id,
            text=content,
            metadata={
                "title": file.filename,
                "file_type": "pdf",
                "original_filename": file.filename
            }
        )
        
        if success:
            logger.info(f"Successfully uploaded and processed PDF '{file.filename}' with ID {content_id}")
            return {
                "message": f"PDF '{file.filename}' successfully uploaded and processed", 
                "content_id": content_id
            }
        else:
            logger.error(f"Failed to process PDF '{file.filename}'")
            raise HTTPException(status_code=500, detail="Failed to process PDF")
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading PDF: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the ingestion service
    """
    try:
        # Validate configuration
        is_valid, message = Config.validate_config()
        if not is_valid:
            logger.warning(f"Configuration validation failed: {message}")
            return {"status": "unhealthy", "details": message}
        
        return {"status": "healthy", "service": "RAG Ingestion API"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}