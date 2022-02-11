"""Define the tests of the rss adapter."""

import random
from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer
from tenacity import RetryError
from werkzeug.wrappers import Response
from werkzeug.wrappers.request import Request

from airss.adapters.extractors import RSS
from airss.model import Article, Source


def faulty_server(request: Request) -> Response:
    """Define the response of a faulty server."""

    if random.random() > 0.5:
        return Response("Error", status=404)

    with open("tests/assets/blue-book-rss.xml", "r") as file_descriptor:
        return Response(file_descriptor.read(), content_type="application/xml")


@pytest.mark.freeze_time()
class TestRSS:
    def test_get_rss(
        self,
        httpserver: HTTPServer,
    ) -> None:
        """
        Given: A working rss feed url with the content of the Blue Book site
        When: fetched with the adapter
        Then: The list of articles are returned
        """
        now = datetime.now()
        with open("tests/assets/blue-book-rss.xml", "r") as file_descriptor:
            httpserver.expect_request("/feed").respond_with_data(
                file_descriptor.read(), content_type="application/xml"
            )

        source, articles = RSS().get(httpserver.url_for("/feed"))

        desired_source = Source(
            title="The Blue Book",
            description="My personal digital garden",
            created_at=now,
            updated_at=datetime.fromtimestamp(1642656915.0),
            next_update_at=None,
            score=None,
            url="https://lyz-code.github.io/blue-book",
            tags=[],
        )
        assert source == desired_source
        assert len(articles) == 16
        assert articles[0] == Article(
            title="19th January 2022",
            created_at=now,
            published_at=datetime.fromtimestamp(1642656915.0),
            updated_at=datetime.fromtimestamp(1642656915.0),
            url="https://lyz-code.github.io/blue-book/newsletter/2022_01_19/",
            author="Lyz",
            summary="article description",
            source_id=None,
        )

    def test_get_retrieve_tags(
        self,
        httpserver: HTTPServer,
    ) -> None:
        """
        Given: An rss with tags in the entries
        When: fetched with the adapter
        Then: The articles have the tags populated
        """
        with open("tests/assets/gaming_on_linux.xml", "r") as file_descriptor:
            httpserver.expect_request("/feed").respond_with_data(
                file_descriptor.read(), content_type="application/xml"
            )

        _, articles = RSS().get(httpserver.url_for("/feed"))

        assert articles[0].tags == ["Open Source", "Wine", "Apps", "Meta"]

    def test_get_raises_error_if_404(
        self,
        httpserver: HTTPServer,
    ) -> None:
        """
        Given: An rss that returns a 404
        When: fetched with the adapter
        Then: an error is raised
        """
        httpserver.expect_request("/feed").respond_with_data("error", status=404)

        with pytest.raises(RetryError) as error:
            RSS().get(httpserver.url_for("/feed"))

    def test_get_retries_if_response_not_200(
        self,
        httpserver: HTTPServer,
    ) -> None:
        """
        Given: An rss that randomly returns a 404 or 200,
        When: fetched with the adapter
        Then: The data is extracted
        """
        httpserver.expect_request("/feed").respond_with_handler(faulty_server)

        source, _ = RSS().get(httpserver.url_for("/feed"))

        assert source.title == "The Blue Book"