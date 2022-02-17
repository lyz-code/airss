"""Define the API."""

import logging
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, Response, UploadFile
from fastapi.logger import logger
from repository_orm import Repository, load_repository

from .. import services
from ..config import Config
from ..model import Article, Source

# Configure logging

log = logging.getLogger("gunicorn.error")
logger.handlers = log.handlers
if __name__ != "main":
    logger.setLevel(log.level)
else:
    logger.setLevel(logging.DEBUG)

# Create main app

app = FastAPI()

# Dependencies


@lru_cache()
def get_config() -> Config:
    """Configure the program settings."""
    # no cover: the dependency are injected in the tests
    log.info("Loading the config")
    return Config()  # pragma: no cover


def get_repo(config: Config = Depends(get_config)) -> Repository:
    """Configure the repository.

    Returns:
        Configured Repository instance.
    """
    log.info("Loading the repository")

    repo = load_repository(config.database_url, [Source, Article])

    return repo


# Endpoints


@app.get("/alive")
def alive() -> Response:
    """Return Always.

    Used to see if the application is running.
    """
    return Response(content="Always")


@app.post("/source/add", status_code=201)
def add_source(source: Source, repo: Repository = Depends(get_repo)) -> None:
    """Record a new source.

    Args:
        source: Media source information.
        repo: Repository to store the data.
    """
    try:
        services.fetch_source_articles(source, repo)
    except Exception:
        repo.close()
        raise HTTPException(
            status_code=409, detail=f"Error fetching source {str(source)}"
        )
    repo.close()


@app.post("/opml/add", status_code=201)
def add_opml(opml: UploadFile, repo: Repository = Depends(get_repo)) -> None:
    """Import the sources of an OPML file.

    Args:
        opml: OPML file.
        repo: Repository to store the data.
    """
    services.import_opml(opml, repo)
    repo.close()
