"""Main API v1 router."""

from fastapi import APIRouter
from ...features.properties.api import router as properties_router
# New routers to be added
from ...features.payments.api import router as payments_router
from ...features.auctions.api import router as auctions_router
from ...features.users.api import router as users_router

# Create main v1 router
api_router = APIRouter(prefix="/api/v1")

# Include feature routers
api_router.include_router(properties_router, tags=["properties"])
api_router.include_router(auctions_router, tags=["auctions"])  # /api/v1/auctions
api_router.include_router(payments_router)   # /api/v1/payment - preserve internal tags
api_router.include_router(users_router, tags=["users"])         # /api/v1/users

# Health check endpoint
@api_router.get("/health")
async def health_check():
	"""Health check endpoint."""
	return {"status": "healthy", "version": "1.0.0"}