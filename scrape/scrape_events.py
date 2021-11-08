"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml
import json
import datetime

EVENTS_SRC_DIR = 'src/_events'
EVENTS_OUT_PATH = 'data/events.tab'

READ_FIELDS = [
    'title',
    'starts',
    'ends',
    'external',
    'organiser',   # email, name
    'location',    # dict
    'tags',        # relation
    'supporters',  # relation
]

WRITE_COLUMNS = [
    'id',
    'date',
    'title',
    'starts',
    'ends',
    'external',
    'organiser_name',
    'organiser_email',
    'address',
    'body',
]


def write_event(i, date_str, meta, body):
    """Write an event item as a csv row."""
    line = [i, date_str]

    for f in READ_FIELDS:
        v = meta.get(f)

        if f == 'organiser':
            if not v:
                line.append('')
                line.append('')
            elif type(v) == str:
                line.append(v)
                line.append('')
            else:
                line.append(v.get('name', ''))
                line.append(v.get('email', ''))
            continue

        if not v:
            line.append('')
            continue

        if f in ('tags', 'supporters'):
            make_event_relations(i, f, v)
            continue

        if f == 'location':
            if type(v) == str:
                v = {'name': v.title()}
            value = json.dumps(v)
        elif type(v) == datetime.date:
            value = v.strftime('%Y-%m-%d')
        elif type(v) == str:
            value = v
        else:
            raise ValueError(f'Unexpected type for field {f}: {type(v)}')
        line.append(value)

    if body:
        line.append(csv_escape(body))

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


def csv_escape(text):
    """Escape functional characters in text for embedding in CSV."""
    return '"' + text.replace('"', '\\"') + '"'


def parse_date(path):
    """Parse date from filename."""
    fname = os.path.basename(path)
    date = fname[:10]
    # Assert dt format
    datetime.datetime.strptime(date, '%Y-%m-%d')
    return date


with open(EVENTS_OUT_PATH, 'w') as f:
    f.write('\t'.join(WRITE_COLUMNS) + '\n')

for f in ('data/event_supporters.tab', 'data/event_tags.tab'):
    if os.path.exists(f):
        os.remove(f)

events_src_paths = [
    os.path.join(EVENTS_SRC_DIR, x)
    for x in os.listdir(EVENTS_SRC_DIR)
    if x.endswith('.md')
]

for i, path in enumerate(sorted(events_src_paths)):
    with open(path) as f:
        content = f.read()
        try:
            meta_str, body = [x for x in content.split('---\n', 2) if x]
        except ValueError:
            meta_str = [x for x in content.split('---\n', 2) if x][0]
            body = None
        meta = yaml.load(meta_str, Loader=yaml.FullLoader)
    print(f'Writing event {i}')
    date_str = parse_date(path)
    write_event(i, date_str, meta, body)
