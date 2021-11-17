"""Generic filters and parsers."""

import re


def get_blurb_from_markdown(text, style=True):
    """Extract a blurb from the first lines of some markdown text."""
    if not text:
        return None

    text = text.replace('\r\n', '\n')

    lines = text.split('\n\n')
    blurb = lines[0]

    if style:
        return blurb

    # Strip style tags
    p = re.compile(r'<style>[\w\W]+</style>', re.MULTILINE)
    matches = p.findall(blurb)
    for m in matches:
        blurb = blurb.replace(m, '')
    return blurb
