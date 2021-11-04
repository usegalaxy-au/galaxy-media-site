"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml
from copy import deepcopy


def recursive_merge(x, y):
    """Perform recursive merge of dictionaries."""
    if not (type(x) == dict and type(y) == dict):
        if not (type(x) == dict or type(y) == dict):
            return
        if not type(x) == dict:
            return y
        if not type(y) == dict:
            return x
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = recursive_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z


fname = 'src/_events/2018-07-17-GTN-cofest.md'
events_path = 'src/_events'
events_files = [
    os.path.join(events_path, x)
    for x in os.listdir(events_path)
    if x.endswith('.md')
]

merged_meta = {}

for fname in events_files:
    with open(fname) as f:
        content = f.read()
        try:
            meta_str, body = [x for x in content.split('---\n', 2) if x]
        except ValueError:
            meta_str = [x for x in content.split('---\n', 2) if x][0]
            body = None
        meta = yaml.load(meta_str, Loader=yaml.FullLoader)
    merged_meta = recursive_merge(merged_meta, meta)
