"""Main API v1 router."""

from fastapi import APIRouter
from ...features.properties.api import router as properties_router

# Create main v1 router
api_router = APIRouter(prefix="/api/v1")

# Include feature routers
api_router.include_router(properties_router, tags=["properties"])

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}