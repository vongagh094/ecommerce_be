"""Database dependencies."""

from typing import Generator
from sqlalchemy.orm import Session
from ...db.sessions.session import SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()