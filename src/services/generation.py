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
            logger.error(f"Generation failed: {e}")
            return "I'm sorry, I encountered an error while generating the response."
