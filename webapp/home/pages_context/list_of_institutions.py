"""Context for rendering list-of-institutions.html"""

from utils.institution import get_institutions


def build_context():
    """Return context for rendering list of institutions."""
    return {'institutions': get_institutions()}
