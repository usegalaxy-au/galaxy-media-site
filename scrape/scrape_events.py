"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml

import parse

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
    # In order of django database table
    # Map django columns to Jekyll meta key or parser function
    ('id', 'id'),
    ('datetime_created', 'date'),
    ('title', 'title'),
    ('body', 'body'),
    ('organiser_name', parse.organiser_name),
    ('organiser_email', parse.organiser_email),
    ('timezone', None),
    ('external', 'external'),
    ('date_end', parse.date_start),
    ('date_start', parse.date_end),
    ('time_end', None),
    ('time_start', None),
    ('address', parse.location_json),
]


def write_event(meta):
    """Write an event item as a csv row."""
    line = []
    for col, key in WRITE_COLUMNS:
        if type(key) == str:
            val = meta.get(key, '')
        elif key is None:
            val = ''
        else:
            val = key(meta)
        line.append(str(val).strip())

    with open(EVENTS_OUT_PATH, 'a') as f:
        f.write('\t'.join(line) + '\n')

    for k in ('tags', 'supporters'):
        make_event_relations(k, meta)


def make_event_relations(k, meta):
    """Create relations between event and other <k> with names <v>.

    This table can be bulk-imported to Django M2M through table once other
    names have been text-replaced with the corresponding pk.
    """
    i = meta['id']
    v = meta.get(k)

    if not v:
        return

    with open(f'data/event_{k}.tab', 'a') as f:
        if type(v) == str:
            f.write(f'{i}\t{v}\n')
        elif type(v) == list:
            for name in v:
                f.write(f'{i}\t{name}\n')


with open(EVENTS_OUT_PATH, 'w') as f:
    f.write('\t'.join([x[0] for x in WRITE_COLUMNS]) + '\n')

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
    print(f'Writing event {i + 1}')
    meta['id'] = i + 1
    meta['date'] = parse.date_from_filepath(path)
    meta['body'] = parse.csv_escape(body).replace(
        'src="/assets',
        'src="/media/uploads',
    )
    write_event(meta)
