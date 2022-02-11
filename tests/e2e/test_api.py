"""Test the API implementation."""

from pytest_httpserver import HTTPServer


class TestAddSource:
    def test_add_source(
        self,
        httpserver: HTTPServer,
    ) -> None:
        """
        Given: An RSS url.
        When: Calling the add endpoint.
        Then: The Source data and it's articles are stored in the repository.
        """
        with open("tests/assets/blue-book-rss.xml", "r") as file_descriptor:
            httpserver.expect_request("/feed").respond_with_data(
                file_descriptor.read(), content_type="application/xml"
            )
