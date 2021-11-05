"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml
import json
import datetime

NEWS_SRC_DIR = 'src/_news'
NEWS_OUT_PATH = 'data/news.tab'

READ_FIELDS = [
    'title',
    'external',
    'tags',
    'supporters',
]

WRITE_COLUMNS = [
    'id',
    'title',
]


def write_event(i, meta, body):
    """Write an event item as a csv row."""
    line = [i]
    for f in READ_FIELDS:
        if f not in meta:
            line.append('')
            continue
        v = meta[f]
        if f == 'organiser':
            if type(v) == str:
                line.append(v)
            elif v is None:
                line.append('')
            else:
                for attr in ('name', 'email'):
                    line.append(v.get(attr, ''))
            continue
        elif f in ('tags'):
            make_event_relations(i, f, v)
            continue
        elif type(v) == dict:
            value = json.dumps(v)
        elif type(v) == datetime.date:
            value = v.strftime('%Y-%m-%d')
        elif type(v) == str:
            value = v
        elif v is None:
            value = ''
        else:
            raise ValueError(f'Unexpected type for field {f}: {type(v)}')
        line.append(value)
    with open(EVENTS_OUT_PATH, 'a') as f:
        f.write('\t'.join([
            str(x) for x in line
        ]) + '\n')


def make_event_relations(i, k, v):
    """Create relations between event and other <k> with names <v>.

    This table can be bulk-imported to Django M2M through table once other
    names have been text-replaced with the corresponding pk.
    """
    with open(f'data/event_{k}.tab', 'a') as f:
        if type(v) == str:
            f.write(f'{i}\t{v}\n')
        elif type(v) == list:
            for name in v:
                f.write(f'{i}\t{name}\n')


with open(EVENTS_OUT_PATH, 'w') as f:
    f.write('\t'.join(WRITE_COLUMNS) + '\n')

for f in ('data/event_supporters.tab', 'data/event_tags.tab'):
    if os.path.exists(f):
        os.remove(f)

events_src_files = [
    os.path.join(EVENTS_SRC_DIR, x)
    for x in os.listdir(EVENTS_SRC_DIR)
    if x.endswith('.md')
]

for i, fname in enumerate(sorted(events_src_files)):
    with open(fname) as f:
        content = f.read()
        try:
            meta_str, body = [x for x in content.split('---\n', 2) if x]
        except ValueError:
            meta_str = [x for x in content.split('---\n', 2) if x][0]
            body = None
        meta = yaml.load(meta_str, Loader=yaml.FullLoader)
    print(f'Writing event {i}')
    write_event(i, meta, body)


###

# from copy import deepcopy


# def recursive_merge(x, y):
#     """Perform recursive merge of dictionaries."""
#     if not (type(x) == dict and type(y) == dict):
#         if not (type(x) == dict or type(y) == dict):
#             return
#         if not type(x) == dict:
#             return y
#         if not type(y) == dict:
#             return x
#     z = {}
#     overlapping_keys = x.keys() & y.keys()
#     for key in overlapping_keys:
#         z[key] = recursive_merge(x[key], y[key])
#     for key in x.keys() - overlapping_keys:
#         z[key] = deepcopy(x[key])
#     for key in y.keys() - overlapping_keys:
#         z[key] = deepcopy(y[key])
#     return z
