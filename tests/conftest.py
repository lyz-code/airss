"""Store the classes and fixtures used throughout the tests."""

from typing import Generator

import freezegun
import pytest
from freezegun.api import FrozenDateTimeFactory
from py._path.local import LocalPath
from pytest_httpserver import HTTPServer
from repository_orm import TinyDBRepository

from airss.model import Article, Source


@pytest.fixture(name="db_tinydb")
def db_tinydb_(tmpdir: LocalPath) -> str:
    """Create an TinyDB database engine.

    Returns:
        database_url: Url used to connect to the database.
    """
    # ignore: Call of untyped join function in typed environment.
    # Until they give typing information there is nothing else to do.
    tinydb_file_path = str(tmpdir.join("tinydb.db"))  # type: ignore
    return f"tinydb:///{tinydb_file_path}"


@pytest.fixture(name="repo")
def repo_(db_tinydb: str) -> Generator[TinyDBRepository, None, None]:
    """Return an instance of the TinyDBRepository."""
    repo = TinyDBRepository([Source, Article], db_tinydb)
    yield repo
    repo.db_.close()


@pytest.fixture(name="_rss")
def _rss_(httpserver: HTTPServer) -> None:
    """Configure the rss feeds.

    * /blue/feed: returns the blue book RSS feed
    * /gaming_on_linux/feed: returns the gaming on linux RSS feed
    * /404: Returns an 404 error

    """
    with open("tests/assets/blue-book-rss.xml", "r") as file_descriptor:
        httpserver.expect_request("/blue/feed").respond_with_data(
            file_descriptor.read(), content_type="application/xml"
        )
    with open("tests/assets/gaming_on_linux.xml", "r") as file_descriptor:
        httpserver.expect_request("/gaming_on_linux/feed").respond_with_data(
            file_descriptor.read(), content_type="application/xml"
        )
    httpserver.expect_request("/404").respond_with_data("error message", status=404)


@pytest.fixture(autouse=True)
def frozen_time() -> Generator[FrozenDateTimeFactory, None, None]:
    """Freeze all tests time"""
    with freezegun.freeze_time() as freeze:
        yield freeze
