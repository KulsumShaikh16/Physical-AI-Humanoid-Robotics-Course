import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.db.neon_client import get_db, Base, engine
from src.db.qdrant_client import get_qdrant_client
from src.services.embedding import EmbeddingService
from src.services.storage import StorageService
from src.services.ingestion import IngestionService
from src.core.logging import logger
from src.models.domain import TextbookContent, SectionMetadata

def get_sample_content():
    """
    Returns sample textbook content for testing ingestion.
    """
    sample_data = [
        TextbookContent(
            text="Welcome to 'Physical AI & Humanoid Robotics'. This book explores the intersection of artificial intelligence and physical embodiment. We cover everything from the philosophy of embodied intelligence to the practical mathematics of humanoid control strings. Our goal is to empower the next generation of robotics engineers to build machines that can interact naturally with the human world.",
            metadata=SectionMetadata(
                title="Preface - Introduction to Physical AI",
                chapter="Introduction",
                section="Preface",
                page_number=1
            )
        ),
        TextbookContent(
            text="Chapter 1: The Evolution of Humanoid Robots. Humanoid robotics is a branch of robotics dedicated to the design, construction, and operation of robots with an anthropomorphic form. Unlike industrial arms, humanoids must balance, walk, and navigate human-centric environments. This chapter provides a historical context from pre-modern automata to modern server-driven humanoid platforms like Atlas and Digit.",
            metadata=SectionMetadata(
                title="Chapter 1 - Historical Context",
                chapter="Introduction to Humanoid Robotics",
                section="1.1 History and Evolution",
                page_number=45
            )
        ),
        TextbookContent(
            text="Inverse kinematics (IK) is the mathematical process of calculating the variable joint parameters needed to place the end of a kinematic chain, such as a robot's hand or foot, in a given position and orientation relative to the start of the chain. In humanoid robotics, IK is critical for foot placement and reaching tasks, requiring complex Jacobian matrices and optimization algorithms.",
            metadata=SectionMetadata(
                title="Control - Inverse Kinematics",
                chapter="Kinematics",
                section="3.2 Inverse Kinematics",
                page_number=88
            )
        ),
        TextbookContent(
            text="Zero Moment Point (ZMP) allows us to determine the stability of a humanoid robot during walking. If the ZMP remains within the support polygon (the area covered by the feet), the robot will not tip over. The ZMP is the point on the ground where the net moment of the inertial and gravitational forces has no component along the horizontal axes. It is a fundamental concept in humanoid balance control.",
            metadata=SectionMetadata(
                title="Locomotion - ZMP Stability",
                chapter="Locomotion and Control",
                section="5.4 ZMP Stability Criterion",
                page_number=112
            )
        )
    ]
    return sample_data

def init_db():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

def main():
    logger.info("Starting ingestion script...")
    
    # Init DB schema
    init_db()
    
    # Instantiate services
    db = next(get_db())
    qdrant = get_qdrant_client()
    
    embedding_service = EmbeddingService()
    storage_service = StorageService(qdrant, db)
    ingestion_service = IngestionService(embedding_service, storage_service)
    
    # Get content
    content = get_sample_content()
    
    # Run ingestion
    ingestion_service.ingest_content(content)
    
    print("Ingestion script finished successfully.")

if __name__ == "__main__":
    main()
