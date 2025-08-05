"""Database configuration."""

from sqlmodel import create_engine, SQLModel
from .config import settings

# Create database engine
engine = create_engine(
    settings.postgres_db.url,
    echo=settings.app.debug,
    pool_pre_ping=True,
    pool_recycle=300
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)