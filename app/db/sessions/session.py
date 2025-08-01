from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings
import redis

settings = get_settings()


engine = create_engine(settings.postgres_db.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_session() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

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
