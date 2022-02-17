"""Test the API implementation."""

from datetime import datetime, timedelta
from textwrap import dedent

import pytest
from fastapi.testclient import TestClient
from py._path.local import LocalPath
from pytest_httpserver import HTTPServer
from repository_orm import Repository

from airss.config import Config
from airss.entrypoints.api import app, get_config
from airss.model import Article, FetchLog, Source


@pytest.fixture(name="client")
def client_(db_tinydb: str) -> TestClient:
    """Configure FastAPI TestClient."""

    def override_config() -> Config:
        """Inject the testing database in the application settings."""
        return Config(database_url=db_tinydb)

    app.dependency_overrides[get_config] = override_config
    return TestClient(app)


def test_alive(client: TestClient) -> None:
    """
    Given: The API backend
    When: alive is called
    Then: always is returned
    """
    result = client.get("/alive")

    assert result.status_code == 200
    assert result.text == "Always"


@pytest.mark.freeze_time()
@pytest.mark.usefixtures("_rss")
class TestAddSource:
    """Test the adding of a source."""

    def test_add_source_minimal(
        self,
        client: TestClient,
        httpserver: HTTPServer,
        repo: Repository,
    ) -> None:
        """
        Given: An RSS url.
        When: Calling the add endpoint with the minimum data.
        Then: The Source data and it's articles are stored in the repository and a
            trace of the good fetch is added in the repository.
        """
        now = datetime.now()
        url = httpserver.url_for("/blue/feed")
        desired_source = Source(
            id_=0,
            url=url,
            title="The Blue Book",
            state="available",
            description="My personal digital garden",
            created_at=now,
            updated_at=datetime(2022, 1, 20, 5, 35, 15),
            next_update_at=now + timedelta(hours=24),
            update_frequency=24,
            score=None,
            tags=[],
        )

        result = client.post(
            "/source/add",
            json={"url": url},
        )

        assert result.status_code == 201
        source = repo.last(Source)
        assert source == desired_source
        articles = repo.all(Article)
        assert len(articles) == 16
        assert articles[0] == Article(
            id_=0,
            title="19th January 2022",
            state="unread",
            created_at=now,
            published_at=datetime(2022, 1, 20, 5, 35, 15),
            updated_at=datetime(2022, 1, 20, 5, 35, 15),
            url="https://lyz-code.github.io/blue-book/newsletter/2022_01_19/",
            author="Lyz",
            preview_score=None,
            predicted_preview_score=None,
            score=None,
            predicted_score=None,
            tags=[],
            summary="article description",
            content=None,
            source_id=0,
        )
        log_entries = repo.all(FetchLog)
        assert log_entries == [
            FetchLog(
                id_=0,
                url=url,
                extractor="RSS",
                created_at=datetime.now(),
                status_code=200,
                message=None,
            )
        ]

    def test_add_source_maximal(
        self, client: TestClient, repo: Repository, httpserver: HTTPServer
    ) -> None:
        """
        Given: An RSS url.
        When: Calling the add endpoint with the maximum data.
        Then: The Source data is stored in the repository.
        """
        now = datetime.now()
        source_data = {
            "url": httpserver.url_for("/blue/feed"),
            "title": "Blue Book",
            "description": "description",
            "update_frequency": 1,
            "score": 4,
            "tags": ["linux", "python"],
        }
        desired_source = Source(
            id_=0,
            url=source_data["url"],
            title=source_data["title"],
            state="available",
            description=source_data["description"],
            created_at=now,
            updated_at=datetime(2022, 1, 20, 5, 35, 15),
            next_update_at=now + timedelta(hours=1),
            update_frequency=source_data["update_frequency"],
            score=source_data["score"],
            tags=source_data["tags"],
        )

        result = client.post(
            "/source/add",
            json=source_data,
        )

        assert result.status_code == 201
        source = repo.last(Source)
        assert source == desired_source

    def test_add_source_handles_fetch_error(
        self,
        client: TestClient,
        httpserver: HTTPServer,
        repo: Repository,
    ) -> None:
        """
        Given: An RSS url that returns an error.
        When: Calling the add endpoint.
        Then: The Source data is stored with status error and a trace of the wrong
            fetch is added in the repository.
        """
        now = datetime.now()
        url = httpserver.url_for("/404")
        desired_source = Source(
            id_=0,
            url=url,
            state="error",
            created_at=now,
            updated_at=None,
            next_update_at=now + timedelta(hours=24),
        )

        result = client.post(
            "/source/add",
            json={"url": url},
        )

        assert result.status_code == 409
        source = repo.last(Source)
        assert source == desired_source
        log_entries = repo.all(FetchLog)
        assert log_entries == [
            FetchLog(
                id_=0,
                url=url,
                extractor="RSS",
                created_at=datetime.now(),
                status_code=404,
                message=f"Url {url} returned an 404 status code",
            )
        ]


@pytest.mark.usefixtures("_rss")
class TestAddOPML:
    """Test the add of an opml file."""

    def test_add_opml(
        self,
        client: TestClient,
        repo: Repository,
        httpserver: HTTPServer,
        tmpdir: LocalPath,
    ) -> None:
        """
        Given: An OMPL file.
        When: Calling the add endpoint with an example file.
        Then: The Source data of each entry and it's articles are stored in
            the repository. The Source's tags are extracted from the OPML categories
            in lowercase
        """
        url_1 = httpserver.url_for("/blue/feed")
        url_2 = httpserver.url_for("/gaming_on_linux/feed")
        opml_file = tmpdir.join("feeds.opml")  # type: ignore
        opml_file.write(
            dedent(
                f"""\n
            <?xml version="1.0" encoding="UTF-8"?>
            <opml version="1.1">
            <head>
                <title>
                Feeder
                </title>
            </head>
            <body>
                <outline title="Linux" text="Linux">
                    <outline title="Blue Book" text="Blue" type="rss" xmlUrl="{url_1}"/>
                </outline>
                <outline title="Python" text="Python">
                    <outline title="Yellow" text="Yellow" type="rss" xmlUrl="{url_2}"/>
                </outline>
            </body>
            </opml>
            """
            )
        )
        with open(opml_file, "rb") as opml_file_descriptor:

            result = client.post(
                "/opml/add",
                files=[("opml", opml_file_descriptor)],
            )

        assert result.status_code == 201
        sources = repo.all(Source)
        assert sources[0].tags == ["linux"]
        assert sources[1].tags == ["python"]
        assert len(sources) == 2
        articles = repo.all(Article)
        assert len(articles) == 66
        log_entries = repo.all(FetchLog)
        assert len(log_entries) == 2
