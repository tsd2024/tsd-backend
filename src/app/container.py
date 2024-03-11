from dependency_injector import containers, providers

from src.database.database import Database


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(Database, db_url=config.database_url)
