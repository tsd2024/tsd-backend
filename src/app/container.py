from dependency_injector import containers, providers

from src.database.database import Database
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(Database, db_url=config.database_url)

    packet_handler_factory = providers.Singleton(
        PacketHandlerFactory
    )
