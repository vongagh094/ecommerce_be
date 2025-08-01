from dependency_injector import containers, providers
from app.db.sessions.session import get_db_session,get_redis, get_rabbitmq_stream
from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.auction_repository import AuctionRepository
from app.db.repositories.redis_repository import RedisRepository
from app.services.auction_service import AuctionService
from app.services.bid_service import BidService
from app.services.rabbitMQ_service import RabbitMQService
from app.services.redis_service import RedisService
class Container(containers.DeclarativeContainer):
    # Database
    db_session = providers.Resource(get_db_session)
    db_redis = providers.Resource(get_redis)

    # RabbitMQ
    rabbitmq_stream = providers.Resource(get_rabbitmq_stream)


    #Repositories
    bid_repository = providers.Factory(
        BidRepository,
        db=db_session
    )

    auction_repository = providers.Factory(
        AuctionRepository,
        db=db_session
    )
    redis_repository = providers.Factory(
        RedisRepository,
        redis_client=db_redis
    )

    # Services
    bid_service = providers.Factory(
        BidService,
        bid_repository=bid_repository
    )
    auction_service = providers.Factory(
        AuctionService,
        auction_repository=auction_repository,
    )
    rabbitMQStream_service = providers.Factory(
        RabbitMQService,
        stream_property=rabbitmq_stream
    )
    redis_service = providers.Factory(
        RedisService,
        redis_repository=redis_repository
    )