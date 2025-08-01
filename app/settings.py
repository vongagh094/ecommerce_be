from decouple import config
from typing import Optional

# Database Configuration
DATABASE_URL = config(
    "DATABASE_URL", 
    default="postgresql://postgres:nhomec123@localhost:5432/ecommerce_db"
)

# Application Configuration
APP_NAME = config("APP_NAME", default="Ecommerce Backend API")
APP_VERSION = config("APP_VERSION", default="1.0.0")
DEBUG = config("DEBUG", default=False, cast=bool)

# Security Configuration
SECRET_KEY = config("SECRET_KEY", default="your-secret-key-change-this-in-production")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)

# CORS Configuration
ALLOWED_ORIGINS = config(
    "ALLOWED_ORIGINS", 
    default="http://localhost:3000,http://127.0.0.1:3000",
    cast=lambda v: [i.strip() for i in v.split(',')]
) 