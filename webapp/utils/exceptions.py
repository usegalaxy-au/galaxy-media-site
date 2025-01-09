"""Custom exceptions."""


class ResourceAccessError(Exception):
    """Raised when a user attempts to access a resource they do not own."""
    pass
