"""Test the API implementation."""

import pytest
from fastapi.testclient import TestClient
from repository_orm import Repository

from airss.config import Config
from airss.entrypoints.api import app
from airss.model import Source


@pytest.fixture(name="client")
def client_(db_tinydb: str) -> TestClient:
    """Configure FastAPI TestClient."""

    def override_config() -> Config:
        """Inject the testing database in the application settings."""
        return Config(database_url=db_tinydb)

    app.dependency_overrides[get_config] = override_config
    return TestClient(app)


@pytest.mark.freeze_time()
class TestAddSource:
    def test_add_source(
        self,
        client: TestClient,
        repo: Repository,
    ) -> None:
        """
        Given: An RSS url.
        When: Calling the add endpoint.
        Then: The Source data and it's articles are stored in the repository.
        """
        source_data = {
            "url": "https://lyz-code.github.io/blue-book/daily.xml",
            "title": "Blue Book",
        }
        result = client.post(
            "/source/add/",
            headers={"X-Token": "coneofsilence"},
            json=source_data,
        )

        assert result.status_code == 201
        source = repo.last(Source)
        assert source.url == source_data["url"]
        assert source.title == source_data["title"]
