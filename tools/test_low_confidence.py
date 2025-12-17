import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_low_confidence():
    print("Testing /chat/query with nonsense (low confidence) query...")
    
    # Nonsense question should hopefully have low vector similarity
    query_payload = {
        "text": "What is the capital of Mars according to jellyfish?"
    }
    
    try:
        response = client.post("/chatbot/query", json=query_payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Request successful. Score: {data['confidence_score']}")
            print(f"Answer: {data['answer']}")
            
            if data['confidence_score'] < 0.3 or "not confident" in data['answer']:
                print("[OK] Low confidence handler triggered correctly.")
                return True
            else:
                print(f"[WARNING] High confidence was reported for nonsense: {data['confidence_score']}")
                return False
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

if __name__ == "__main__":
    test_low_confidence()
