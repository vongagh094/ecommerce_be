from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload
from app.api.bidding import bidding
from app.features.messages.api.conversation_routes import router as conversation_router
from app.features.messages.api.message_routes import router as message_router
from app.features.messages.api.pusher_config_routes import router as pusher_config_router
from app.features.wishlist.api.wishlist_routes import router as wishlist_router
from app.features.property.api.property_routes import router as property_router
from app.features.property.api.property_amenity_routes import router as property_amenity_router
from app.features.property.api.property_type_routes import router as property_type_router
from app.features.property.api.property_category_routes import router as property_category_router
from app.features.notification.api.notification_routes import router as notification_router
from app.api.auction import router as auction_router
from app.core.container import Container
from app.services.CORS import setup_cors
from app.api.review import router as review_router
from app.api.calendar import router as calendar_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[
        "app.api.bidding",
        "app.features.messages.api.conversation_routes",
        "app.features.messages.api.message_routes",
        "app.features.messages.api.pusher_config_routes",
        "app.features.wishlist.api.wishlist_routes",
        "app.features.property.api.property_routes",
        "app.features.property.api.property_amenity_routes",
        "app.features.property.api.property_type_routes",
        "app.features.property.api.property_category_routes",
        "app.features.notification.api.notification_routes",
        "app.api.review",
        "app.api.auction",
        "app.api.calendar"
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
    app.include_router(conversation_router, prefix="/conversations", tags=["Conversations"])
    app.include_router(message_router, prefix="/messages", tags=["Messages"])
    app.include_router(pusher_config_router, prefix="/pusher", tags=["Pusher Config"])
    app.include_router(wishlist_router, prefix="/wishlist", tags=["Wishlist"])
    app.include_router(property_router, prefix="/properties", tags=["Properties"])
    app.include_router(property_amenity_router, prefix="/property-amenities", tags=["Property Amenities"])
    app.include_router(property_type_router, prefix="/property-types", tags=["Property Types"])
    app.include_router(property_category_router, prefix="/property-categories", tags=["Property Categories"])
    app.include_router(review_router, prefix="/reviews", tags=["Reviews"])
    app.include_router(calendar_router, prefix="/calendar", tags=["Calendar"])
    app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])
    app.include_router(auction_router, prefix="/auctions", tags=["Auctions"])
    return app

app = create_app()