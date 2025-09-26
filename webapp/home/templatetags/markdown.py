"""Markdown rendering with python-markdown2.

https://github.com/trentm/python-markdown2
"""

import markdown2
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def render_markdown(md):
    if not md:
        return ""
    html = markdown2.markdown(md.strip(), extras={
        "tables": True,
        "code-friendly": True,
        "html-classes": {
            'table': 'table table-striped',
        },
    })
    return html.strip(' \n')


@register.filter()
def markdown(md):
    """Render html from markdown string."""
    html = render_markdown(md)
    return mark_safe(html)


@register.filter()
def inline_markdown(md):
    """Render markdown to HTML and strip enclosing <p> tags."""
    html = render_markdown(md)
    if html.startswith('<p>'):
        html = html[3:-4]
    return mark_safe(html)
