"""Dependency injection container."""

from dependency_injector import containers, providers
from pusher import Pusher
from app.features.messages.core.settings import get_settings
from app.db.sessions.session import get_db_session, get_redis, get_rabbitmq_stream
from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.auction_repository import AuctionRepository
from app.features.messages.repositories.message_repository import MessageRepository
from app.features.messages.repositories.conversation_repository import ConversationRepository
from app.features.property.repositories.amenity_repository import AmenityRepository
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.features.property.repositories.property_repository import PropertyRepository
from app.features.wishlist.repositories.wishlist_repository import WishlistRepository
from app.db.repositories.redis_repository import RedisRepository
from app.services.auction_service import AuctionService
from app.services.bid_service import BidService
from app.features.messages.services.message_service import MessageService
from app.features.messages.services.pusher_service import PusherService
from app.features.property.services.property_service import PropertyService
from app.features.property.services.property_amenity_service import PropertyAmenityService
from app.features.property.services.property_image_service import PropertyImageService
from app.features.wishlist.services.wishlist_service import WishlistService
from app.services.rabbitMQ_service import RabbitMQService
from app.services.redis_service import RedisService
from app.ws_integration.notifier import WebSocketNotifier


class Container(containers.DeclarativeContainer):
    # Config
    config = providers.Singleton(get_settings)

    # Pusher
    pusher = providers.Singleton(
        Pusher,
        app_id=config.provided["PUSHER_APP_ID"],
        key=config.provided["PUSHER_KEY"],
        secret=config.provided["PUSHER_SECRET"],
        cluster=config.provided["PUSHER_CLUSTER"],
        ssl=True
    )

    # WebSocket notifier
    ws_notifier = providers.Singleton(WebSocketNotifier)

    # Pusher Service
    pusher_service = providers.Factory(
        PusherService,
        pusher=pusher
    )

    # Database
    db_session = providers.Resource(get_db_session)
    db_redis = providers.Resource(get_redis)

    # RabbitMQ
    rabbitmq_stream = providers.Resource(get_rabbitmq_stream)
    
    # Repositories
    bid_repository = providers.Factory(
        BidRepository,
        db=db_session
    )
    
    auction_repository = providers.Factory(
        AuctionRepository,
        db=db_session
    )

    message_repository = providers.Factory(
        MessageRepository,
        db=db_session
    )
    
    conversation_repository = providers.Factory(
        ConversationRepository,
        db=db_session
    )
    
    property_amenity_repository = providers.Factory(
        PropertyAmenityRepository,
        db=db_session
    )
    
    property_image_repository = providers.Factory(
        PropertyImageRepository,
        db=db_session
    )
    
    amenity_repository = providers.Factory(
        AmenityRepository,
        db=db_session
    )
    
    wishlist_repository = providers.Factory(
        WishlistRepository,
        db=db_session
    )
    
    wishlist_property_repository = providers.Factory(
        WishlistRepository,
        db=db_session
    )
        
    redis_repository = providers.Factory(
        RedisRepository,
        redis_client=db_redis
    )

    property_repository = providers.Factory(
        PropertyRepository,
        db=db_session,
        property_amenity_repository=property_amenity_repository,
        property_image_repository=property_image_repository
    )
    
    # Services
    bid_service = providers.Factory(
        BidService,
        bid_repository=bid_repository
    )
    
    auction_service = providers.Factory(
        AuctionService,
        auction_repository=auction_repository
    )

    message_service = providers.Factory(
        MessageService,
        message_repository=message_repository,
        conversation_repository=conversation_repository,
        pusher_service=pusher_service
    )
    
    rabbitMQStream_service = providers.Factory(
        RabbitMQService,
        stream_property=rabbitmq_stream
    )

    redis_service = providers.Factory(
        RedisService,
        redis_repository=redis_repository
    )

    property_service = providers.Factory(
        PropertyService,
        property_repository=property_repository,
        property_amenity_repository=property_amenity_repository,
        property_image_repository=property_image_repository
    )

    property_amenity_service = providers.Factory(
        PropertyAmenityService,
        property_amenity_repository=property_amenity_repository,
        amenity_repository=amenity_repository
    )

    property_image_service = providers.Factory(
        PropertyImageService,
        property_image_repository=property_image_repository
    )

    wishlist_service = providers.Factory(
        WishlistService,
        wishlist_repository=wishlist_repository,
        wishlist_property_repository=wishlist_property_repository
    )
    
    # Wire payment and booking services with WebSocket notifier
    def wire_payment_service(self, service):
        """Wire WebSocket notifier to payment service."""
        service.set_ws_notifier(self.ws_notifier())
        return service
    
    def wire_booking_service(self, service):
        """Wire WebSocket notifier to booking service."""
        service.set_ws_notifier(self.ws_notifier())
        return service