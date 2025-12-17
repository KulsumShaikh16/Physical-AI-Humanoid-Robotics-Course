
# Quickstart Guide: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This guide will help you quickly set up and run the RAG chatbot for the Physical AI & Humanoid Robotics textbook.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to OpenAI API (or similar LLM provider)
- Qdrant vector database (can run locally or remotely)

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your API keys and configuration
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

3. **Install and run Qdrant locally (optional)**:
   ```bash
   # Using Docker
   docker run -p 6333:6333 -p 6334:6334 \
     -v ./qdrant_storage:/qdrant/storage:z \
     qdrant/qdrant
   ```

## Loading Textbook Content

1. **Add textbook content** to the designated directory:
   ```bash
   # Place your textbook files in the content directory
   # Supported formats: .txt, .pdf, .md
   ```

2. **Ingest textbook content into the vector database**:
   ```bash
   python -m src.api.ingestion_router --input-path path/to/textbook/content
   ```

## Running the Application

1. **Start the API server**:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

2. **Test the API endpoints**:
   ```bash
   # Test chat endpoint
   curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the key components of humanoid robotics?"
     }'
   ```

## API Usage

### Chat Endpoint
Send questions to the chatbot:
```
POST /chat
{
  "query": "Your question about the textbook content"
}
```

### Ingestion Endpoint
Add new textbook content:
```
POST /ingest
{
  "content": "Textbook content to be ingested",
  "metadata": {
    "title": "Chapter Title",
    "section": "Section Name"
  }
}
```

## Environment Configuration

The following environment variables need to be set:

- `OPENAI_API_KEY`: Your OpenAI API key for LLM interactions
- `QDRANT_URL`: URL for your Qdrant vector database instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `EMBEDDING_MODEL`: The embedding model to use (default: text-embedding-ada-002)
- `LLM_MODEL`: The LLM model to use for generation (default: gpt-3.5-turbo)

## Next Steps

- Review the full API documentation at `/docs` when the server is running
- Customize the system for your specific textbook content
- Adjust the embedding and LLM models based on your requirements
- Set up monitoring and logging for production use