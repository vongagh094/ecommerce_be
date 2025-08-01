# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.bidding import bidding
from app.core.container import Container
from app.services.CORS import setup_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[
        "app.api.bidding"
    ])
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Ecommerce Backend API",
        description="A professional FastAPI ecommerce backend with PostgreSQL",
        version="1.0.0",
        lifespan=lifespan
    )
    setup_cors(app)
    app.container = container
    app.include_router(bidding)
    return app

app = create_app()