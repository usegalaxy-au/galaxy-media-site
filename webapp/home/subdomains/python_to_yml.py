"""Parse content encoded in Python as write to YAML file.

genome.sections
genome.content.data
genome.content.assembly
genome.content.annotation

"""

import re
import yaml
import genome
from pathlib import Path


class LiteralUnicode(str):
    pass


def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


def format_section(section):
    """Find HTML items and strip whitespace from them."""
    new_section = section.copy()
    for tab_ix, tab in enumerate(section['tabs']):
        if isinstance(tab['content'], list):
            for ix, item in enumerate(tab['content']):
                for k, v in item.items():
                    if 'html' in k:
                        new_section['tabs'][tab_ix]['content'][ix][k] = (
                            strip_html_whitespace(v)
                        )
        else:
            # content is in subsections
            for subsection_ix, subsection in enumerate(
                tab['content']['subsections']
            ):
                for ix, item in enumerate(subsection['content']):
                    for k, v in item.items():
                        if 'html' in k:
                            new_section[
                                'tabs'][tab_ix]['content']['subsections'][
                                    subsection_ix]['content'][ix][k] = (
                                strip_html_whitespace(v)
                            )
    return new_section


def strip_html_whitespace(html):
    """Remove whitespace from HTML string.

    Replace multiple spaces with single space.
    """
    return re.sub(
        r'\s+', ' ',
        html.replace('\n', '').replace('\\', ''),
    ).strip()


# yaml.add_representer(LiteralUnicode, literal_unicode_representer)

for section in genome.sections:
    section = format_section(section)
    fname = Path(__file__).parent / f"{section['id']}.yml"
    with open(fname, 'w') as f:
        yaml.dump(section, f)
