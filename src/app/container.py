from dependency_injector import containers, providers

from src.database.database import Database
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(Database, db_url=config.database_url)

    packet_handler_factory = providers.Singleton(
        PacketHandlerFactory
    )

    redis_handler = providers.Singleton(
        RedisHandler,
        connection_string=config.redis_connection_string
    )
