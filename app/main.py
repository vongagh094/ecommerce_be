# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.config import settings
from app.core.container import Container
from app.shared.middleware import add_error_handlers, setup_cors
from app.api.v1.router import api_router
from app.api.bidding import bidding  # Keep existing bidding functionality

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app.title,
        description=settings.app.description,
        version=settings.app.version,
        debug=settings.app.debug,
        lifespan=lifespan
    )
    
    # Setup middleware
    setup_cors(app)
    add_error_handlers(app)
    
    # Setup dependency injection
    container = Container()
    container.wire(modules=[
        "app.api.bidding",
        "app.features.properties.api.property_api"
    ])
    app.container = container
    
    # Include routers
    app.include_router(api_router)  # New API structure
    app.include_router(bidding)     # Existing bidding functionality
    
    return app

app = create_app()