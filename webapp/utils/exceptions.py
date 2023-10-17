"""Custom exceptions."""


class ResourceAccessError(Exception):
    """Raised when a user attempts to access a resource they do not own."""

    def __init__(self, message):
        """Initialize the exception."""
        super().__init__(message)
