"""Define the program exceptions."""


class FetchError(Exception):
    """Model errors when fetching content from the sources."""

    def __init__(self, message: str, status_code: int) -> None:
        """Initialize the exception."""
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
