from typing import List
import logging
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for handling text embedding operations using either OpenAI or a Hugging Face embedding model
    """

    def __init__(self):
        # Check for OpenAI API key first
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key and "your_openai" in openai_api_key:
            openai_api_key = None

        if openai_api_key:
            # Use OpenAI embeddings if available
            try:
                from langchain_openai import OpenAIEmbeddings
            except ImportError:
                try:
                    from langchain_community.embeddings import OpenAIEmbeddings
                except ImportError:
                    from langchain.embeddings import OpenAIEmbeddings
            
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=openai_api_key
            )
            self.use_openai = True
        else:
            # Fallback to Hugging Face embedding model if OpenAI key not available
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
            except ImportError:
                from langchain.embeddings import HuggingFaceEmbeddings
                
            # Use the model specified in the environment variable, default to all-MiniLM-L6-v2
            model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            self.use_openai = False

        # Initialize text splitter for chunking large documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def create_embeddings(self, text: str) -> List[float]:
        """
        Create embeddings for a given text
        """
        try:
            if self.use_openai:
                embedding = self.embeddings.embed_query(text)
            else:
                # For Hugging Face embeddings
                embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    def create_document_embeddings(self, documents: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of documents
        """
        try:
            if self.use_openai:
                embeddings = self.embeddings.embed_documents(documents)
            else:
                # For Hugging Face embeddings
                embeddings = [self.embeddings.embed_query(doc) for doc in documents]
            return embeddings
        except Exception as e:
            logger.error(f"Error creating document embeddings: {str(e)}")
            raise

    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks that are appropriate for embedding
        """
        try:
            texts = self.text_splitter.split_text(text)
            return texts
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise