# Chatbot Service

This directory contains the backend service for the RAG (Retrieval-Augmented Generation) chatbot. The chatbot uses Cohere for embeddings and chat, and Qdrant for vector search.

## How it works

1.  **Ingestion**: The `ingest.py` script reads the content of the textbook from the `my-website/docs` directory, creates embeddings using the Cohere API, and stores them in a Qdrant collection.
2.  **Backend**: The `main.py` script starts a FastAPI server that exposes a `/chat` endpoint. This endpoint takes a user query, creates an embedding for the query, searches for relevant context in the Qdrant collection, and then uses the Cohere chat model to generate an answer based on the context.
3.  **Frontend**: The frontend is a React component in `my-website/src/components/Chatbot.tsx` that makes requests to the backend service.

## How to run

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up environment variables**:
    Create a `.env` file in this directory and add the following environment variables:
    ```
    COHERE_API_KEY=your_cohere_api_key
    QDRANT_URL=your_qdrant_url
    QDRANT_API_KEY=your_qdrant_api_key
    ```
3.  **Run the ingestion script**:
    ```bash
    python ingest.py
    ```
4.  **Start the backend service**:
    ```bash
    uvicorn main:app --reload
    ```
5.  **Run the frontend**:
    Navigate to the `my-website` directory and run:
    ```bash
    npm install
    npm start
    ```
The website will be available at `http://localhost:3000`. The chatbot will be available as a widget on the website.
