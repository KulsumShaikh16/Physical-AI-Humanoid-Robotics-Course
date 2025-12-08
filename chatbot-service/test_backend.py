import requests
import sys

def test_backend():
    base_url = "http://localhost:8000"
    
    print(f"Testing backend at {base_url}...")
    
    # 1. Test Health
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("[OK] Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"[FAIL] Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to backend. Is it running?")
        print("   Try running: python -m uvicorn main:app --reload")
        return False

    # 2. Test Chat
    try:
        payload = {"query": "Hello"}
        response = requests.post(f"{base_url}/chat", json=payload)
        if response.status_code == 200:
            print("[OK] Chat endpoint passed!")
            data = response.json()
            print(f"   Answer: {data.get('answer')[:100]}...") # Print preview
        else:
            print(f"[FAIL] Chat endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Error testing chat endpoint: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)
