"""Store the classes and fixtures used throughout the tests."""

import pytest
from py._path.local import LocalPath
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
def repo_(db_tinydb: str) -> TinyDBRepository:
    """Return an instance of the TinyDBRepository."""
    return TinyDBRepository([Source, Article], db_tinydb)
