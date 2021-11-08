"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml
import json
import datetime

NEWS_SRC_DIR = 'src/_posts'
NEWS_OUT_PATH = 'data/news.tab'

READ_FIELDS = [
    'title',
    'external',
    'tags',
    'supporters',
]

WRITE_COLUMNS = [
    'id',
    'date',
    'title',
    'external',
    'body',
]


def write_news(i, date_str, meta, body):
    """Write an news item as a csv row."""
    line = [i, date_str]
    for f in READ_FIELDS:
        v = meta.get(f)
        if not v:
            line.append('')
            continue
        if f in ('tags', 'supporters'):
            make_news_relations(i, f, v)
            continue
        elif type(v) == dict:
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

    with open(NEWS_OUT_PATH, 'a') as f:
        f.write('\t'.join([
            str(x) for x in line
        ]) + '\n')


def make_news_relations(i, k, v):
    """Create relations between news and other <k> with names <v>.

    This table can be bulk-imported to Django M2M through table once other
    names have been text-replaced with the corresponding pk.
    """
    with open(f'data/news_{k}.tab', 'a') as f:
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
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except Exception:
        raise ValueError(f"Couldn't parse date from filename {fname}")
    return date


with open(NEWS_OUT_PATH, 'w') as f:
    f.write('\t'.join(WRITE_COLUMNS) + '\n')

for f in ('data/news_supporters.tab', 'data/news_tags.tab'):
    if os.path.exists(f):
        os.remove(f)

news_src_paths = [
    os.path.join(NEWS_SRC_DIR, x)
    for x in os.listdir(NEWS_SRC_DIR)
    if x.endswith('.md')
]

for i, path in enumerate(sorted(news_src_paths)):
    with open(path) as f:
        content = f.read()
        try:
            meta_str, body = [x for x in content.split('---\n', 2) if x]
        except ValueError:
            meta_str = [x for x in content.split('---\n', 2) if x][0]
            body = None
        meta = yaml.load(meta_str, Loader=yaml.FullLoader)
    print(f'Writing news {i}')
    date_str = parse_date(path)
    write_news(i, date_str, meta, body)
