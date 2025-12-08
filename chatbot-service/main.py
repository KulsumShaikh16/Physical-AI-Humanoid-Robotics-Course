import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Clients
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not COHERE_API_KEY:
    print("Warning: COHERE_API_KEY not found in environment variables")
if not QDRANT_URL:
    print("Warning: QDRANT_URL not found in environment variables")

try:
    co = cohere.Client(COHERE_API_KEY)
    # Connect to Qdrant Cloud or local
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
except Exception as e:
    print(f"Failed to initialize clients: {e}")
    co = None
    qdrant = None

COLLECTION_NAME = "ai_textbook"

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    if not co or not qdrant:
        raise HTTPException(status_code=503, detail="AI Services not initialized")

    try:
        # 1. Embed Query
        response = co.embed(texts=[request.query], model="embed-english-v3.0", input_type="search_query")
        embedding = response.embeddings[0]

        # 2. Search Qdrant
        search_result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            limit=3,
            with_payload=True
        ).points

        context = ""
        if search_result:
            context = "\n".join([hit.payload.get("text", "") for hit in search_result])
        
        if not context:
            context = "No specific context found in the book."

        # 3. Generate Answer
        prompt = f"""You are an helpful AI assistant for the 'AI Native Development' book. 
        Use the following context from the book to answer the user's question. 
        If the answer is not in the context, say you don't know but try to be helpful based on general knowledge if appropriate, but flag it.
        
        Context:
        {context}
        
        Question: {request.query}
        
        Answer:"""

        chat_response = co.chat(
            message=prompt,
            model="command-r-plus-08-2024",
            temperature=0.3
        )

        return {
            "answer": chat_response.text, 
            "context": [hit.payload for hit in search_result] if search_result else []
        }

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok", "cohere": co is not None, "qdrant": qdrant is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
