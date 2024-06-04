"""Custom exceptions."""


class ResourceAccessError(Exception):
    """Raised when a user attempts to access a resource they do not own."""
    pass


class SubsiteBuildError(Exception):
    """Raised when an error occurs during subsite build."""

    def __init__(self, message, description=''):
        """Initialize the exception."""
        message = (
            "<h1>Galaxy Lab build error</h1>"
            "<br>"
            f"<p>{message}<p>"
            f"<p>{description}</p>"
        )
        super().__init__(message)
