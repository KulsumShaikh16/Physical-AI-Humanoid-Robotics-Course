from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.config import get_settings
from src.db.neon_client import get_db
from src.db.qdrant_client import get_qdrant_client
from src.api.chatbot_router import router as chatbot_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    health_status = {"status": "healthy", "components": {}}
    
    # Check Postgres
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["postgres"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["postgres"] = f"error: {str(e)}"
        
    # Check Qdrant
    try:
        q_client = get_qdrant_client()
        q_client.get_collections()
        health_status["components"]["qdrant"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["qdrant"] = f"error: {str(e)}"
        
    if health_status["status"] == "degraded":
        raise HTTPException(status_code=503, detail=health_status)
        
    return health_status

@app.get("/")
def root():
    return {"message": "Welcome to AI Textbook RAG Chatbot API"}
