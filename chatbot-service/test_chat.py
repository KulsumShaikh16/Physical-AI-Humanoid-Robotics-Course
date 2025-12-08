import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/chat",
        json={"query": "What is embodied intelligence?"},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:", json.dumps(response.json(), indent=2))
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Failed to connect: {e}")
