import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def verify_chapter_answering():
    print("Verifying if /chatbot/query handles 'Chapter 1' correctly...")
    
    query_payload = {
        "text": "What is Chapter 1 about?"
    }
    
    try:
        response = client.post("/chatbot/query", json=query_payload)
        
        if response.status_code == 200:
            data = response.json()
            score = data['confidence_score']
            answer = data['answer']
            
            print(f"Match Score: {score}")
            print(f"Answer: {answer[:300]}...")
            
            # Check if it was refused
            if "not confident" in answer.lower() and score < 0.15:
                print("[FAILED] Chatbot still refusing Chapter 1 query.")
                return False
            elif score >= 0.15:
                print("[SUCCESS] Chatbot accepted query with score above 0.15.")
                if len(answer) > 100:
                     print("[SUCCESS] Received a substantial answer.")
                return True
            else:
                print(f"[NOTE] Score was {score}, which is below 0.15. If it still refuses, this is expected for extremely low scores.")
                return False
        else:
            print(f"[ERROR] Request failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

if __name__ == "__main__":
    verify_chapter_answering()
