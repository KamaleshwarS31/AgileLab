from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        # checkfirst=True will only create tables if they don't exist
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Database tables verified/created successfully")
    except Exception as e:
        print(f"Warning: Database initialization issue: {e}")
        # Don't fail startup if tables already exist
        pass

