#!/usr/bin/env python3

"""Collect all tags and supporters from m2m tables."""

LJUST = 25

with open('data/event_supporters.tab') as f:
    supporters = [
        line.split('\t')[1].strip(' \n') for line in f
    ]

with open('data/news_supporters.tab') as f:
    supporters += [
        line.split('\t')[1].strip(' \n') for line in f
    ]

with open('data/event_tags.tab') as f:
    tags = [
        line.split('\t')[1].strip(' \n') for line in f
    ]

with open('data/news_tags.tab') as f:
    tags += [
        line.split('\t')[1].strip(' \n') for line in f
    ]

supporters = sorted(list({
    x for x in supporters if x
}))

tags = sorted(list({
    x for x in tags if x
}))

both = [
    f"{s.ljust(LJUST)}| {t}"
    for s, t in zip(supporters[:len(tags)], tags)
] + [x.ljust(LJUST) + '|' for x in supporters[len(tags):]]

with open('data/supporters_list.txt', 'w') as f:
    f.write('\n'.join(supporters))

with open('data/tags_list.txt', 'w') as f:
    f.write('\n'.join(tags))

with open('data/both_list.txt', 'w') as f:
    f.write("Supporters".ljust(LJUST) + "| Tags\n")
    f.write('-' * 51 + '\n')
    f.write('\n'.join(both))

print('Done')
