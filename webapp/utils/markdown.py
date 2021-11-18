"""Generic filters and parsers."""

import re

# To render/replace image URIs
IMAGE_URI_EXPRESIONS = (
    {   # markdown image tags
        're': r'\(img\d\)',  # regex to match
        'tag': '(img{i})',   # format string to replace
    },
    {   # html image tags
        're': r'src="img\d"',
        'tag': 'src="img{i})"',
    },
)


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


def render_image_uri(instance):
    """Render image URIs over markdown placeholders."""
    body = instance.body

    for e in IMAGE_URI_EXPRESIONS:
        p = re.compile(e.re, re.MULTILINE)
        m = p.search(instance.body)
        if not m:
            # No tags to replace
            continue

        # Determine current instance image number
        i = 1
        while e.tag.format(i) not in instance.body:
            i += 1

        # Replace placeholder with real URI
        body = body.replace(
            e.tag.format(i),
            e.tag.format(instance.img_uri))

    return body
