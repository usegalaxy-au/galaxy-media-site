"""Add missing OIDS to relation tables."""


paths = [
    'data/event_supporters_ids.tab',
    'data/event_tags_ids.tab',
    'data/news_supporters_ids.tab',
    'data/news_tags_ids.tab',
]

for p in paths:
    with open(p) as f:
        lines = [
            f"{i + 1}\t{x}"
            for i, x in enumerate(f)
        ]
    with open(p.replace('_ids', '_oids'), 'w') as f:
        f.write(''.join(lines))

print('Done')
