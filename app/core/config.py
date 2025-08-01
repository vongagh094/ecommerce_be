import os
from functools import lru_cache
from pydantic import Field, BaseModel

class PostgresConfig(BaseModel):
    url: str = Field(default="postgresql://postgres:postgres@localhost:5432/postgres")

class RedisConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)
    retry_count: int = Field(default=3)
    lock_expire: int = Field(default=5)
class RabbitMQConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=5552)
    username: str = Field(default="guest")
    password: str = Field(default="guest")
    stream_name: str = Field(default="bidding_stream")
    stream_retention: int = Field(default=1000000)  # Retention in bytes
class AppConfig(BaseModel):
    title: str = Field(default="Ecommerce Backend API")
    description: str = Field(default="A professional FastAPI ecommerce backend")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000, ge=1, le=65535)
    reload: bool = Field(default=True)

class Settings(BaseModel):
    postgres_db: PostgresConfig = PostgresConfig()
    redis_db: RedisConfig = RedisConfig()
    rabbit_mq: RabbitMQConfig = RabbitMQConfig()
    app: AppConfig = AppConfig()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

@lru_cache()
def get_settings() -> Settings:
    database_url = (
        os.getenv("DATABASE__URL") or
        os.getenv("DATABASE_URL") or
        "postgresql://postgres:nhomec123@localhost:5432/ecommerce_db"
    )
    return Settings(
        postgres_db=PostgresConfig(
            url=database_url
        ),
        redis_db=RedisConfig(
            host=os.getenv("REDIS__HOST", "localhost"),
            port=int(os.getenv("REDIS__PORT", 6379)),
            db=int(os.getenv("REDIS__DB", 0)),
            retry_count=int(os.getenv("REDIS__RETRY", 3)),
            lock_expire=int(os.getenv("REDIS__LOCK_EXPIRE", 5))  # Lock expire in seconds
        ),
        rabbit_mq=RabbitMQConfig(
            host=os.getenv("RABBITMQ__HOST", "localhost"),
            port=int(os.getenv("RABBITMQ__PORT", 5552)),
            username=os.getenv("RABBITMQ__USERNAME", "admin"),
            password=os.getenv("RABBITMQ__PASSWORD", "admin"),
            stream_name=os.getenv("RABBITMQ__STREAM_NAME", "bidding_stream"),
            stream_retention=int(os.getenv("RABBITMQ__STREAM_RETENTION", 5000000)) # Retention in bytes
        ),
        app=AppConfig(
            version=os.getenv("APP__VERSION", "1.0.0"),
            debug=os.getenv("APP__DEBUG", "false").lower() in ("true", "1", "yes"),
            host=os.getenv("APP__HOST", "127.0.0.1"),
            port=int(os.getenv("APP__PORT", 8000))
        )
    )