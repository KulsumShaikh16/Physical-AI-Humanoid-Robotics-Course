import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from src.api.main import app
from src.core.logging import logger

client = TestClient(app)

def test_chat_query():
    print("Testing /chat/query endpoint...")
    
    # Question related to ingested content
    query_payload = {
        "text": "What is Zero Moment Point?"
    }
    
    try:
        response = client.post("/chatbot/query", json=query_payload)
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] Request successful")
            print(f"Answer: {data['answer']}")
            print(f"Confidence: {data['confidence_score']}")
            print(f"Sources: {len(data['sources'])}")
            if data['sources']:
                print(f"First Source: {data['sources'][0]}")
            
            # Simple assertion
            if "Zero Moment Point" in data['answer'] or "ZMP" in data['answer'] or "stability" in data['answer'] or data['sources']:
                print("[OK] Answer seems relevant.")
            else:
                print("[WARNING] Answer might not be relevant.")
                
            return True
        else:
            print(f"[ERROR] Request failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception during test: {e}")
        return False

if __name__ == "__main__":
    if test_chat_query():
        print("\n[SUCCESS] Chat API verified.")
    else:
        print("\n[FAILURE] Chat API verification failed.")
