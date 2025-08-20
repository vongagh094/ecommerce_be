from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import get_settings
import redis
from contextlib import asynccontextmanager

# Define Base before importing models
Base = declarative_base()

# Import all models to ensure they're registered with SQLAlchemy
try:
    from app.db.models import *
except ImportError:
    # Models might not be available during initial setup
    pass

settings = get_settings()


engine = create_engine(settings.postgres_db.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous SQLAlchemy setup
async_engine = create_async_engine(settings.postgres_db.url.replace("postgresql://", "postgresql+asyncpg://"), echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

def get_db_session() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
        
from typing import AsyncGenerator

@asynccontextmanager
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get asynchronous database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

# REDIS
def get_redis():
    r = redis.Redis(host=settings.redis_db.host,port=settings.redis_db.port,db=settings.redis_db.db)
    max_try = settings.redis_db.retry_count
    lock_expire = settings.redis_db.lock_expire
    try:
        yield r,max_try, lock_expire
    finally:
        r.close()
# RABBITMQ
def get_rabbitmq_stream():
    """Get RabbitMQ stream configuration"""
    return {
        "host": settings.rabbit_mq.host,
        "port": settings.rabbit_mq.port,
        "username": settings.rabbit_mq.username,
        "password": settings.rabbit_mq.password,
        "stream_name": settings.rabbit_mq.stream_name,
        "stream_retention": settings.rabbit_mq.stream_retention
        }
