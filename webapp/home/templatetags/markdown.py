"""Markdown rendering with python-markdown2.

https://github.com/trentm/python-markdown2
"""

import markdown2
from django import template

register = template.Library()


@register.filter()
def markdown(md):
    """Render html from markdown string."""
    if not md:
        return ""
    html = markdown2.markdown(md, extras={
        "tables": True,
        "code-friendly": True,
        "html-classes": {
            'table': 'table table-striped',
        },
    })
    return html
