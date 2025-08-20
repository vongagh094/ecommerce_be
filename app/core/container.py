from dependency_injector import containers, providers
from pusher import Pusher
from app.features.messages.core.settings import get_settings
from app.db.sessions.session import get_db_session, get_redis, get_rabbitmq_stream, get_async_db_session
from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.auction_repository import AuctionRepository
from app.features.messages.repositories.message_repository import MessageRepository
from app.features.messages.repositories.conversation_repository import ConversationRepository
from app.features.property.repositories.amenity_repository import AmenityRepository
from app.features.property.repositories.property_amenity_repository import PropertyAmenityRepository
from app.features.property.repositories.property_image_repository import PropertyImageRepository
from app.features.property.repositories.property_repository import PropertyRepository
from app.features.wishlist.repositories.wishlist_repository import WishlistRepository
from app.features.notification.repositories.notification_repository import NotificationRepository
from app.db.repositories.booking_repository import BookingRepository
from app.db.repositories.redis_repository import RedisRepository
from app.services.auction_service import AuctionService
from app.services.booking_service import BookingService
from app.services.bid_service import BidService
from app.features.messages.services.message_service import MessageService
from app.features.messages.services.pusher_service import PusherService
from app.features.property.services.property_service import PropertyService
from app.features.property.services.property_amenity_service import PropertyAmenityService
from app.features.property.services.property_image_service import PropertyImageService
from app.features.wishlist.services.wishlist_service import WishlistService
from app.features.notification.services.notification_service import NotificationService
from app.services.rabbitMQ_service import RabbitMQService
from app.services.redis_service import RedisService
from app.db.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService
from app.db.repositories.calender_repository import CalendarRepository
from app.services.calendar_service import CalendarService
from app.services.winlose_service import WinLoseService
from app.services.winner_service import WinnerService
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

    # Pusher Service
    pusher_service = providers.Factory(
        PusherService,
        pusher=pusher
    )

    # Database
    db_session = providers.Resource(get_db_session)
    db_redis = providers.Resource(get_redis)
    db_async_session = providers.Resource(get_async_db_session)

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
    review_repository = providers.Factory(
        ReviewRepository,
        db=db_session
    )

    calendar_repository = providers.Factory(
        CalendarRepository,
        db=db_session
    )
    notification_repository = providers.Factory(
        NotificationRepository,
        db=db_session
    )

    booking_repository = providers.Factory(
        BookingRepository,
        db=db_async_session
    )

    # Services
    bid_service = providers.Factory(
        BidService,
        bid_repository=bid_repository
    )

    auction_service = providers.Factory(
        AuctionService,
        auction_repository=auction_repository,
        property_repository=property_repository,
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
    review_service = providers.Factory(
        ReviewService,
        review_repository=review_repository
    )
    calendar_service = providers.Factory(
        CalendarService,
        calendar_repository=calendar_repository,
        bid_repository=bid_repository
    )
    notification_service = providers.Factory(
        NotificationService,
        notification_repository=notification_repository
    )
    
    booking_service = providers.Factory(
        BookingService,
        booking_repository=booking_repository
    )
    winlose_service = providers.Factory(
        WinLoseService,
        auction_repository=auction_repository,
        bid_repository=bid_repository,
    )
    winner_service = providers.Factory(
        WinnerService,
        bid_repository=bid_repository,
        auction_repository=auction_repository
    )
