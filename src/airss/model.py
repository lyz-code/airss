"""Define the data models of the program."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import AnyHttpUrl, Field
from repository_orm import Entity


class ArticleState(str, Enum):
    """Define the possible article states."""

    DELETED = "deleted"
    UNREAD = "unread"
    PREVIEWED = "previewed"
    READ = "read"


class Article(Entity):

    """Define the model of an article."""

    title: str
    state: ArticleState = ArticleState.UNREAD
    created_at: datetime
    published_at: datetime
    updated_at: datetime
    url: AnyHttpUrl
    author: str
    preview_score: Optional[int] = Field(None, gt=0, le=5)
    predicted_preview_score: Optional[int] = Field(None, gt=0, le=5)
    score: Optional[int] = Field(None, gt=0, le=5)
    predicted_score: Optional[int] = Field(None, gt=0, le=5)
    tags: List[str] = Field(default_factory=list)
    summary: Optional[str] = None
    content: Optional[str] = None
    source_id: Optional[int] = None


class SourceState(str, Enum):
    """Define the possible article states."""

    DELETED = "deleted"
    AVAILABLE = "available"


class Source(Entity):
    """Define the model of an article source.

    Args:
        update_frequency: hours between fetches
    """

    url: AnyHttpUrl
    title: str
    state: SourceState = SourceState.AVAILABLE
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    next_update_at: Optional[datetime] = None
    update_frequency: int = 24
    score: Optional[int] = Field(None, gt=0, le=5)
    tags: List[str] = Field(default_factory=list)
