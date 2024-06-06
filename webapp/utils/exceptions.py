"""Custom exceptions."""

import logging
from pprint import pformat

logger = logging.getLogger('django')


class ResourceAccessError(Exception):
    """Raised when a user attempts to access a resource they do not own."""
    pass


class SubsiteBuildError(Exception):
    """Raised when an error occurs during subsite build."""

    def __init__(self, exc=None, url=None, section_id=None, source=''):
        """Initialize the exception."""
        self.title = (
            f"Error parsing {source} content from file"
            if source else None
        )
        self.url = url
        self.message = str(exc)
        self.section_id = section_id

        msg = (
            'Error processing exported lab content\n'
            f'URL: {url}\n'
            f'Errors:\n'
        )

        if hasattr(exc, 'errors'):
            # It's a Pydantic error. Extract info for rendering individual
            # messages
            self.errors = []
            for error in exc.errors():
                err = {
                    'msg': error['msg'],
                    'location': (
                        f'{error["loc"][0]} > '
                        + ' > '.join(str(x) for x in error["loc"][1:])
                    ),
                    'input': pformat(error['input']),
                }
                self.errors.append(err)
            msg += pformat(self.errors)
        else:
            msg += str(exc)

        logger.warning(exc)
        super().__init__(msg)
