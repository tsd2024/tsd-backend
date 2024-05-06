import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

    origins = [
        "https://localhost",
        "https://d359m7qsv8npm1.cloudfront.net/",
        "http://d359m7qsv8npm1.cloudfront.net/",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.container = container
    app.include_router(root_router())
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run('src.app.main:app', host="0.0.0.0", port=80, reload=True)
