"""Return context for given template path."""

from . import (
    list_of_institutions,
)

CONTEXTS = {
    'list-of-institutions.html': list_of_institutions,
}


def get(template_path):
    engine = CONTEXTS.get(template_path)
    if engine:
        return engine.build_context()
