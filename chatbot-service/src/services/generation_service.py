from typing import List, Dict
import logging
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GenerationService:
    """
    Service for generating responses using an LLM based on retrieved content
    """

    def __init__(self):
        # Initialize the language model based on available API keys
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key and "your_openai" in openai_api_key:
            openai_api_key = None

        # Check for Hugging Face token as well
        hf_token = os.getenv("HF_TOKEN")

        if gemini_api_key:
            # Use Google's Gemini API
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_gemini = True
            self.use_openai = False
            self.use_hf = False
        elif openai_api_key:
            # Use OpenAI if Gemini key not available
            from langchain.chat_models import ChatOpenAI
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.3,
                openai_api_key=openai_api_key
            )
            self.use_gemini = False
            self.use_openai = True
            self.use_hf = False
        elif hf_token:
            # Use Hugging Face if other keys not available
            # Note: This assumes you have a text generation model, adjust as needed
            from langchain.llms import HuggingFaceHub
            self.llm = HuggingFaceHub(
                repo_id=os.getenv("GENERATION_MODEL", "Kulsum16/chatbot"),
                huggingfacehub_api_token=hf_token,
            )
            self.use_gemini = False
            self.use_openai = False
            self.use_hf = True
        else:
            # Fallback to a local model if no API keys available
            from langchain.llms import HuggingFacePipeline
            import transformers
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch

            model_id = "gpt2"  # Using a simple local model as fallback
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForCausalLM.from_pretrained(model_id)

            # Set pad token if it doesn't exist
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            pipe = transformers.pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=100,
                device_map="auto" if torch.cuda.is_available() else "cpu"
            )

            self.llm = HuggingFacePipeline(pipeline=pipe)
            self.use_gemini = False
            self.use_openai = False
            self.use_hf = False
            self.use_local = True

        # Define the prompt template for our RAG system
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an AI assistant specialized in answering questions about physical AI and humanoid robotics based on a textbook. Use the provided context to answer the user's question. Be concise and accurate. If the information is not available in the context, clearly state that you don't have enough information to answer the question."),
            HumanMessage(content="Context:\n{context}\n\nQuestion: {question}")
        ])

    def generate_response(self, question: str, context: List[Dict]) -> str:
        """
        Generate a response based on the user's question and the retrieved context
        """
        try:
            # Format the context as a string
            context_str = "\n\n".join([
                f"Title: {item['title']}\nContent: {item['content'][:500]}..."
                for item in context
            ])

            if self.use_gemini:
                # Create a prompt for Gemini
                prompt = f"""
                You are an AI assistant specialized in answering questions about physical AI and humanoid robotics based on a textbook.
                Use the provided context to answer the user's question. Be concise and accurate.
                If the information is not available in the context, clearly state that you don't have enough information to answer the question.

                Context:
                {context_str}

                Question: {question}
                """

                # Generate content using Gemini
                response = self.model.generate_content(prompt)
                return response.text
            elif self.use_openai:
                # Use OpenAI
                # Format the prompt with context and question
                messages = self.prompt_template.format_messages(
                    context=context_str,
                    question=question
                )

                # Generate the response
                response = self.llm(messages)
                return response.content
            elif self.use_hf:
                # For Hugging Face endpoints, format the input differently
                prompt = f"""
                Context: {context_str}

                Question: {question}

                Answer the question based on the context provided. Be concise and accurate.
                """

                # Note: This is a simplified approach; actual implementation would need to match your space's API
                response = self.llm(prompt)
                return str(response)
            else:
                # Use local model
                # Format the prompt with context and question for local model
                messages = self.prompt_template.format_messages(
                    context=context_str,
                    question=question
                )

                # For local models, we'll use the first message content
                prompt = messages[0].content
                response = self.llm(prompt)
                return str(response)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def calculate_confidence(self, context: List[Dict], question: str) -> float:
        """
        Calculate a confidence score for the response based on context relevance
        This is a simplified implementation - in a real system, you'd want more sophisticated metrics
        """
        try:
            if not context:
                return 0.0

            # A simple confidence calculation based on the highest score in the context
            # and the number of relevant pieces
            max_score = max([item.get("score", 0) for item in context])
            avg_score = sum([item.get("score", 0) for item in context]) / len(context)

            # Combine max and average scores to get a confidence value between 0 and 1
            confidence = (max_score * 0.6 + avg_score * 0.4)

            # Ensure the confidence is between 0 and 1
            return min(1.0, max(0.0, confidence))
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            # Return a default confidence in case of error
            return 0.5