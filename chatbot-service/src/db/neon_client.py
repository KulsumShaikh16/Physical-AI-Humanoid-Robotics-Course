from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import get_settings

settings = get_settings()

DATABASE_URL = settings.NEON_DATABASE_URL

engine = create_engine(DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
