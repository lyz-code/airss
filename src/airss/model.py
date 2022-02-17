"""Define the data models of the program."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, Field, root_validator
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
    ERROR = "error"


class Source(Entity):
    """Define the model of an article source."""

    url: AnyHttpUrl
    title: Optional[str] = None
    state: SourceState = SourceState.AVAILABLE
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    next_update_at: datetime
    update_frequency: int
    score: Optional[int] = Field(None, gt=0, le=5)
    tags: List[str] = Field(default_factory=list)

    @root_validator(pre=True)
    @classmethod
    def set_default_values(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Set the created_at and date for the next update."""
        if "created_at" not in values:
            values["created_at"] = datetime.now()
        if "update_frequency" not in values:
            values["update_frequency"] = 24
        if "next_update_at" not in values:
            values["next_update_at"] = values["created_at"] + timedelta(
                hours=values["update_frequency"]
            )
        return values


class FetchLog(Entity):
    """Define the model of a fetch log entry."""

    url: AnyHttpUrl
    extractor: str
    created_at: datetime
    status_code: int = 200
    message: Optional[str] = None
    traceback: Optional[str] = None
