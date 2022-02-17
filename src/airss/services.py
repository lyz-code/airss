"""Define all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING, List, Tuple

from bs4 import BeautifulSoup
from tenacity import RetryError

from .adapters.extractors import RSS
from .model import FetchLog, Source, SourceState

if TYPE_CHECKING:
    from fastapi import UploadFile
    from repository_orm import Repository

    from .model import Article

log = logging.getLogger(__name__)


def fetch_source_articles(source: "Source", repo: "Repository") -> None:
    """Fetch and add the source articles to the repository."""
    log.info(f"Adding source {str(source)}")

    extractor = RSS()
    try:
        new_source, articles = get(repo, extractor, source.url)
    except RetryError as error:
        source.state = SourceState.ERROR
        repo.add(source)
        repo.commit()
        raise error

    # Merge source, new_source and original source with `merge`, make sure that
    # `created_at` is not set by the `extractor.get`, remove L44-L46
    original_source = repo.search({"url": source.url}, [Source])[0]
    source.updated_at = new_source.updated_at

    for attribute in ["title", "description"]:
        if getattr(source, attribute) is None:
            setattr(source, attribute, getattr(new_source, attribute))

    repo.add(source)
    repo.add(articles)  # type: ignore
    repo.commit()


def import_opml(opml_file: "UploadFile", repo: "Repository") -> None:
    """Add the sources and their articles from an OPML file."""
    log.info("Adding sources from OPML file")

    opml = BeautifulSoup(opml_file.file.read(), "lxml").body

    for category in opml.findAll("outline"):
        for source in category.findAll("outline"):
            fetch_source_articles(
                Source(url=source["xmlurl"], tags=[category["title"].lower()]), repo
            )


def get(
    repo: "Repository", extractor: "RSS", url: str
) -> Tuple["Source", List["Article"]]:
    """Use the extractor to get an url and record it's success or failure in the repo.

    Raises:
        RetryError: if the fetch fails.
    """
    fetch_log = FetchLog(
        url=url,
        extractor="RSS",
        created_at=datetime.now(),
    )
    try:
        log.debug(f"Fetching url {url} with extractor {str(extractor)}")
        source, articles = extractor.get(url)
        repo.add(fetch_log)
    except RetryError as retry_error:
        error = retry_error.args[0].exception()
        repo.add(
            fetch_log.copy(
                update={
                    "status_code": error.status_code,
                    "message": error.message,
                }
            )
        )
        log.warning(
            f"Error {error.status_code} fetching url {url} with message {error.message}"
        )

        raise retry_error

    return source, articles
