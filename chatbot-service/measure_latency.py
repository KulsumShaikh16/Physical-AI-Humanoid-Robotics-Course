import time
import asyncio
from src.services.embedding import EmbeddingService
from src.db.qdrant_client import get_qdrant_client
from src.services.retrieval import RetrievalService
from src.services.generation import GenerationService
from src.models.domain import UserQuery

async def main():
    print("Initializing services...", flush=True)
    
    # Initialize services
    t0 = time.time()
    embedding_service = EmbeddingService()
    qdrant_client = get_qdrant_client()
    retrieval_service = RetrievalService(qdrant_client)
    generation_service = GenerationService()
    print(f"Service init time: {time.time() - t0:.4f}s")
    
    query_text = "What is humanoid robotics?"
    print(f"\nProcessing query: '{query_text}'")
    
    # 1. Embed Query
    start_time = time.time()
    query_vector = embedding_service.generate_query_embedding(query_text)
    embed_time = time.time() - start_time
    print(f"LATENCY: Embedding time: {embed_time:.4f}s", flush=True)
    
    # 2. Retrieve Context
    start_time = time.time()
    context_items = retrieval_service.search_similar_content(query_vector)
    retrieve_time = time.time() - start_time
    print(f"LATENCY: Retrieval time: {retrieve_time:.4f}s", flush=True)
    
    if not context_items:
        print("No context found.")
        return

    confidence_score = max([item["score"] for item in context_items])
    print(f"Best Match Score: {confidence_score}")
    
    # 3. Generate Answer
    start_time = time.time()
    answer = generation_service.generate_response(query_text, context_items)
    gen_time = time.time() - start_time
    print(f"LATENCY: Generation time: {gen_time:.4f}s", flush=True)
    print(f"\nTotal time: {embed_time + retrieve_time + gen_time:.4f}s")

if __name__ == "__main__":
    asyncio.run(main())
