"""Scrape Galaxy Australia content from the old static site."""

import os
import yaml

import parse

NEWS_SRC_DIR = 'src/_posts'
NEWS_OUT_PATH = 'data/news.tab'

READ_FIELDS = [
    'title',
    'external',
    'tags',
    'supporters',
]

WRITE_COLUMNS = [
    ('id', 'id'),
    ('datetime_created', 'date'),
    ('title', 'title'),
    ('body', 'body'),
    ('external', 'external'),
]


def write_news(meta):
    """Write an news item as a csv row."""
    line = []
    for col, key in WRITE_COLUMNS:
        if type(key) == str:
            val = meta.get(key, '')
        else:
            val = key(meta)
        line.append(str(val).strip())

    with open(NEWS_OUT_PATH, 'a') as f:
        f.write('\t'.join(line) + '\n')

    for k in ('tags', 'supporters'):
        make_news_relations(k, meta)


def make_news_relations(k, meta):
    """Create relations between news and other <k> with names <v>.

    This table can be bulk-imported to Django M2M through table once other
    names have been text-replaced with the corresponding pk.
    """
    i = meta['id']
    v = meta.get(k)

    with open(f'data/news_{k}.tab', 'a') as f:
        if type(v) == str:
            f.write(f'{i}\t{v}\n')
        elif type(v) == list:
            for name in v:
                f.write(f'{i}\t{name}\n')


with open(NEWS_OUT_PATH, 'w') as f:
    f.write('\t'.join([x[0] for x in WRITE_COLUMNS]) + '\n')

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
    meta['id'] = i
    meta['date'] = parse.date_from_filepath(path)
    meta['body'] = parse.csv_escape(body)
    write_news(meta)
