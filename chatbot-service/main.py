from fastapi import FastAPI
from src.api.chatbot_router import router as chatbot_router
from src.api.ingestion_router import router as ingestion_router

app = FastAPI(
    title="AI Textbook RAG Chatbot API",
    description="A RAG (Retrieval-Augmented Generation) chatbot for answering questions about physical AI and humanoid robotics textbooks",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the RAG chatbot API routes
app.include_router(chatbot_router)
app.include_router(ingestion_router)

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the AI Textbook RAG Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Textbook API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}