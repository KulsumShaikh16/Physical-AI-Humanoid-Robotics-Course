import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print(f"Qdrant URL: {QDRANT_URL}")

try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"Client type: {type(client)}")
    print(f"Has search? {'search' in dir(client)}")
    print("All attributes:")
    print([d for d in dir(client) if not d.startswith('_')])
except Exception as e:
    print(f"Error: {e}")
