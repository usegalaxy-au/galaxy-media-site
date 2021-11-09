"""Generic filters and parsers."""


def get_blurb_from_markdown(text):
    """Extract a blurb from the first lines of some markdown text."""
    if not text:
        return None

    lines = text.split('\n\n')
    blurb = lines[0]
    return blurb
