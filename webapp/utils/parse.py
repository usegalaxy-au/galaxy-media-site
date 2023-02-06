"""Parsing functions."""


def parse_list(string: str, sep=','):
    """Parse a list from a string."""
    if not string:
        return []
    return [
        x.strip()
        for x in string.strip(sep).split(sep)
    ]
