# ADR 3: Dual-Storage RAG Backend and AI Model Selection

## Status
Accepted

## Context
The "Physical AI & Humanoid Robotics" textbook requires a robust RAG (Retrieval-Augmented Generation) chatbot. The backend needs to handle large amounts of technical text, provide high-quality vector search, and generate accurate, context-aware responses while staying within reasonable cost and scalability limits.

## Decision
We decided on the following stack and architecture:
1.  **Dual-Storage Architecture**:
    *   **Relational Data (Text/Metadata)**: Neon Postgres (Serverless) using SQLAlchemy.
    *   **Vector Data (Embeddings)**: Qdrant Cloud (Free Tier) for similarity search.
2.  **Model Selection**:
    *   **Embeddings**: Cohere `embed-english-v3.0` (1024 dimensions).
    *   **Generation**: Gemini 2.0 Flash (`gemini-2.0-flash`).
3.  **Framework**: FastAPI for high-performance asynchronous API endpoints.

## Rationale
*   **Decoupling**: Separating relational metadata from vector indices allows for more flexible queries (e.g., retrieving full chapters or filtering by relational attributes) without overloading the vector database.
*   **Quality**: Cohere's v3 models are specifically designed for search tasks, offering better retrieval performance than generic embedding models.
*   **Efficiency**: Gemini 2.0 Flash provides a state-of-the-art balance of speed, intelligence, and a generous free tier, making it ideal for real-time educational use cases.
*   **Scalability**: Both Neon and Qdrant are serverless/managed solutions, reducing infrastructure management overhead.

## Consequences
*   **Synchronization**: The application layer must ensure that Neon and Qdrant stay synchronized during ingestion (dual-writes).
*   **Network Latency**: Calling two external databases and two AI APIs (Cohere + Gemini) adds cumulative latency, which we mitigated using asynchronous Python and optimized query patterns.
*   **Dependency**: Heavy reliance on multiple third-party SaaS providers.
