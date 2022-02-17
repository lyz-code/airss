"""Define the program factories."""

from typing import Any

from pydantic_factories import ModelFactory

from airss import model


class SourceFactory(ModelFactory[Any]):
    """Define the factory of the Source model"""

    __model__ = model.Source
