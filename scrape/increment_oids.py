"""Add missing OIDS to relation tables."""


paths = [
    'data/event_supporters_oids.tab',
    'data/event_tags_oids.tab',
    'data/news_supporters_oids.tab',
    'data/news_tags_oids.tab',
]

for p in paths:
    with open(p) as f:
        lines = []
        for line in f.read().split('\n'):
            if not line:
                continue
            items = line.split('\t')
            items[1] = str(int(items[1]) + 1)
            lines.append('\t'.join(items))

    with open(p.replace('_oids', '_oids_2'), 'w') as f:
        f.write('\n'.join(lines))

print('Done')
