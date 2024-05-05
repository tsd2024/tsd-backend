from dependency_injector import containers, providers

from src.database.database import Database
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_lobby_state.lobby_state_getter import LobbyStateGetter
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory
from src.usecase.create_lobby import CreateLobbyUseCase
from src.usecase.stories_tickets.add_story import AddStoriesUseCase


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

    lobby_state_getter = providers.Singleton(
        LobbyStateGetter
    )

    create_lobby_use_case = providers.Singleton(
        CreateLobbyUseCase,
        redis_handler=redis_handler
    )

    add_stories_use_case = providers.Singleton(
        AddStoriesUseCase,
        redis_handler=redis_handler
    )