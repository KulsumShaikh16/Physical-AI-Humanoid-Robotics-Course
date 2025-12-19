import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# Get values
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GENERATION_MODEL", "gemini-1.5-flash")

print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found!")
print(f"Model: {model_name}")
print(f"\nTesting Gemini API...\n")

# Test the API
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say hello in one word")
    print(f"✅ SUCCESS! Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
