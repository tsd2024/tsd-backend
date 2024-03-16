import logging

import uvicorn
from fastapi import FastAPI

from src.app.container import Container
from src.app.router import root_router
from src.app.settings import Settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def create_app():
    settings = Settings(_env_file='..env')
    container = Container()
    container.config.from_dict(settings.model_dump())

    database = container.database()
    database.create_database()

    container.wire(packages=['src.app.controller', 'src.app.middleware'])

    app = FastAPI(
        title="Projekt1",
    )

    app.container = container
    app.include_router(root_router())
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run('src.app.main:app', host="0.0.0.0", port=80, reload=True)
