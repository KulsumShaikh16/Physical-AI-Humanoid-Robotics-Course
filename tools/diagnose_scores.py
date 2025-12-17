import sys
import os
sys.path.append(os.getcwd())

from src.services.embedding import EmbeddingService
from src.db.qdrant_client import get_qdrant_client
from src.services.retrieval import RetrievalService

def diagnose_scores():
    queries = [
        "ell me about chapter 1",
        "hat is the context of the book\"",
        "Context of the book",
        "Chapter 1"
    ]
    
    embedding_service = EmbeddingService()
    q_client = get_qdrant_client()
    retrieval_service = RetrievalService(q_client)
    
    for q in queries:
        print(f"\n--- Query: {q} ---")
        vector = embedding_service.generate_query_embedding(q)
        results = retrieval_service.search_similar_content(vector)
        
        if not results:
            print("No results found.")
            continue
            
        for i, res in enumerate(results):
            print(f"Match {i+1}: Score={res['score']} | Title={res['metadata'].title} | Text={res['text'][:100]}...")

if __name__ == "__main__":
    diagnose_scores()
