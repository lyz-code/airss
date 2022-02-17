"""Define the adapters to extract data from the sources."""

import logging
import time
from contextlib import suppress
from datetime import datetime
from typing import List, Tuple

import feedparser
from tenacity import retry
from tenacity.stop import stop_after_attempt

from ..exceptions import FetchError
from ..model import Article, Source

log = logging.getLogger(__name__)


class RSS:
    """Implement the adapter of the RSS sources."""

    @retry(stop=stop_after_attempt(5))
    def get(self, url: str) -> Tuple[Source, List[Article]]:
        """Build the source and article from the feed content.

        Raises:
            FetchError: if the server doesn't return the expected content.
        """
        log.debug(f"Fetching RSS content from {url}")
        now = datetime.now()

        data = feedparser.parse(url)
        if data.status != 200:
            raise FetchError(
                f"Url {url} returned an {data.status} status code",
                status_code=data.status,
            )

        source = Source(
            title=data.feed.title,
            description=data.feed.subtitle,
            created_at=now,
            updated_at=self._feed_time_to_datetime(data.feed.published_parsed),
            url=data.feed.link,
        )

        articles: List[Article] = []
        for entry in data.entries:
            article = Article(
                title=entry.title,
                created_at=now,
                published_at=self._feed_time_to_datetime(entry.published_parsed),
                # using published_at instead of updated_at until the next issue is
                # solved https://github.com/kurtmckee/feedparser/issues/151
                updated_at=self._feed_time_to_datetime(entry.published_parsed),
                url=entry.link,
                author=entry.author,
                summary=entry.summary,
            )

            with suppress(AttributeError):
                article.tags = [tag["term"] for tag in entry.tags]

            articles.append(article)

        return source, articles

    def _feed_time_to_datetime(self, feed_time: time.struct_time) -> datetime:
        """
        Convert feedparser parsed dates into a datetime object.

        Arguments:
            feed_time (feedparser time tuple): time to parse

        Returns:
            datetime: parsed date.
        """
        return datetime.fromtimestamp(time.mktime(feed_time))
