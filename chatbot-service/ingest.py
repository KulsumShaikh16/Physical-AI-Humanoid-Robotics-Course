import os
import glob
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not COHERE_API_KEY:
    print("Error: COHERE_API_KEY not found.")
    exit(1)

try:
    co = cohere.Client(COHERE_API_KEY)
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
except Exception as e:
    print(f"Error initializing clients: {e}")
    exit(1)

COLLECTION_NAME = "ai_textbook"
DOCS_DIR = "../my-website/docs"

def ingest():
    print(f"Connecting to Qdrant at {QDRANT_URL or 'local'}...")
    # Create Collection
    try:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created/reset.")
    except Exception as e:
        print(f"Error creating collection: {e}")
        return

    documents = []
    # Adjust path if running from chatbot-service dir
    search_path = os.path.join(os.path.dirname(__file__), DOCS_DIR)
    files = glob.glob(f"{search_path}/**/*.md", recursive=True)
    
    print(f"Found {len(files)} markdown files in {search_path}")

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Simple chunking: Split by double newlines (paragraphs) and group
            # For robustness, using a fixed character limit overlap is better, but this is a starter
            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
            
            for idx, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50: # Skip empty/small chunks
                    documents.append({
                        "text": chunk,
                        "source": os.path.basename(file_path),
                        "id": f"{os.path.basename(file_path)}_{idx}"
                    })

    print(f"Prepared {len(documents)} chunks. Embedding and indexing...")

    batch_size = 90 # Cohere limit is often 96
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        texts = [d["text"] for d in batch]
        
        try:
            response = co.embed(texts=texts, model="embed-english-v3.0", input_type="search_document")
            embeddings = response.embeddings
            
            points = [
                models.PointStruct(
                    id=abs(hash(d["id"])) % ((2**64) - 1), # Simple hash ID to fits uint64
                    vector=embeddings[j],
                    payload={"text": d["text"], "source": d["source"]}
                )
                for j, d in enumerate(batch)
            ]
            
            qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
            print(f"Indexed batch {(i//batch_size) + 1}/{(len(documents)//batch_size) + 1}")
        except Exception as e:
            print(f"Error indexing batch {i}: {e}")

    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()
