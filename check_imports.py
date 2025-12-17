
try:
    import fastapi
    print("fastapi: installed")
except ImportError:
    print("fastapi: missing")

try:
    import uvicorn
    print("uvicorn: installed")
except ImportError:
    print("uvicorn: missing")

try:
    import torch
    print("torch: installed")
except ImportError:
    print("torch: missing")

try:
    import qdrant_client
    print("qdrant_client: installed")
except ImportError:
    print("qdrant_client: missing")
