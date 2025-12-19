import google.generativeai as genai
from typing import List
from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()

class GenerationService:
    def __init__(self):
        # Configure Gemini
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not found. Generation will fail.")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GENERATION_MODEL)

    def generate_response(self, query: str, context_chunks: List[dict]) -> str:
        """
        Generate a response using Gemini, conditioned on retrieved context.
        """
        try:
            # Construct context string
            context_text = "\n\n".join([
                f"Section: {item['metadata'].section}\nContent: {item['text']}" 
                for item in context_chunks
            ])
            
            prompt = f"""You are an expert AI assistant for a Physical AI and Humanoid Robotics textbook. 
Answer the user's question mostly based on the provided textbook context.
If the context doesn't contain the answer, say "I cannot find the answer in the provided textbook sections." using your best judgement.

Context:
{context_text}

User Question: {query}

Answer:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Generation failed: {error_msg}")
            logger.error(f"Full error details: {repr(e)}")
            logger.info(f"Current model in use: {settings.GENERATION_MODEL}")
            logger.info(f"API key configured: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
            
            if any(indicator in error_msg.lower() for indicator in ["429", "quota", "exhausted", "limit", "resource"]):
                return (
                    "I've reached the current API quota limit for answering questions. "
                    "If you are using 'gemini-2.0-flash' in your .env, please try switching to 'gemini-1.5-flash' "
                    "which has a more stable free tier quota. Otherwise, please try again later."
                )
            
            return f"The generation service encountered an error: {error_msg.split(':', 1)[-1].strip() if ':' in error_msg else error_msg}"

    def generate_response_stream(self, query: str, context_chunks: List[dict]):
        """
        Generate a streaming response using Gemini.
        """
        try:
            # Construct context string
            context_text = "\n\n".join([
                f"Section: {item['metadata'].section}\nContent: {item['text']}" 
                for item in context_chunks
            ])
            
            prompt = f"""You are an expert AI assistant for a Physical AI and Humanoid Robotics textbook. 
Answer the user's question mostly based on the provided textbook context.
If the context doesn't contain the answer, say "I cannot find the answer in the provided textbook sections." using your best judgement.

Context:
{context_text}

User Question: {query}

Answer:"""
            
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Streaming Generation failed: {error_msg}")
            
            if any(indicator in error_msg.lower() for indicator in ["429", "quota", "exhausted", "limit", "resource"]):
                yield (
                    "I've reached the current API quota limit for answering questions. "
                    "Please try again later or check your API configuration."
                )
            else:
                yield f"Error: {error_msg.split(':', 1)[-1].strip() if ':' in error_msg else error_msg}"
