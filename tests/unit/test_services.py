"""Tests the service layer."""

import pytest
from pytest_httpserver import HTTPServer
from repository_orm import Repository
from tenacity import RetryError

from airss import services
from airss.adapters.extractors import RSS
from airss.model import FetchLog


@pytest.mark.usefixtures("_rss")
class TestGet:
    """Test the implementation of the get service."""

    def test_get_records_unhappy_path(
        self, repo: Repository, httpserver: HTTPServer
    ) -> None:
        """
        Given: An url that returns an error
        When: using the get function
        Then: The error is registered and the exception is raised.

            We leave the commit action to the parent functions.
        """
        url = httpserver.url_for("/404")

        with pytest.raises(RetryError):
            services.get(repo, RSS(), url)  # act

        repo.commit()
        log_entries = repo.all(FetchLog)
        assert log_entries == []
