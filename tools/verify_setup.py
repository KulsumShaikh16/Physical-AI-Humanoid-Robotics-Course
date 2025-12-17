import sys
import os
import asyncio
from sqlalchemy import text

# Add project root to path
sys.path.append(os.getcwd())

from src.core.config import get_settings
from src.db.neon_client import get_db
from src.db.qdrant_client import get_qdrant_client
from src.core.logging import logger

def verify_neon():
    print("Verifying Neon Postgres connection...")
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        print("[OK] Neon Postgres connection successful!")
        return True
    except Exception as e:
        print(f"[ERROR] Neon Postgres connection failed: {e}")
        return False

def verify_qdrant():
    print("Verifying Qdrant connection...")
    try:
        client = get_qdrant_client()
        collections = client.get_collections()
        print(f"[OK] Qdrant connection successful! Found {len(collections.collections)} collections.")
        return True
    except Exception as e:
        print(f"[ERROR] Qdrant connection failed: {e}")
        return False

def main():
    logger.info("Starting setup verification...")
    neon_ok = verify_neon()
    qdrant_ok = verify_qdrant()
    
    if neon_ok and qdrant_ok:
        print("\n[SUCCESS] All systems operational!")
        sys.exit(0)
    else:
        print("\n[WARNING] Some systems failed verification.")
        sys.exit(1)

if __name__ == "__main__":
    main()
