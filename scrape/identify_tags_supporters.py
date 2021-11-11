"""Use id_map.json to replace keywords with ids.

Makes *_[tags/supporters].tab ready for DB import.
"""

import json

with open('data/id_map.json') as f:
    data = json.load(f)
with open('data/event_tags.tab') as f:
    event_tags = f.read()
with open('data/event_supporters.tab') as f:
    event_supporters = f.read()
with open('data/news_tags.tab') as f:
    news_tags = f.read()
with open('data/news_supporters.tab') as f:
    news_supporters = f.read()

for name, i in data['tags'].items():
    event_tags = event_tags.replace(f"\t{name}\n", f"\t{str(i)}\n")
    news_tags = news_tags.replace(f"\t{name}\n", f"\t{str(i)}\n")

for name, i in data['supporters'].items():
    event_supporters = event_supporters.replace(
        f"\t{name}\n", f"\t{str(i)}\n")
    news_supporters = news_supporters.replace(
        f"\t{name}\n", f"\t{str(i)}\n")

with open('data/event_tags_ids.tab', 'w') as f:
    f.write(event_tags)
with open('data/event_supporters_ids.tab', 'w') as f:
    f.write(event_supporters)
with open('data/news_tags_ids.tab', 'w') as f:
    f.write(news_tags)
with open('data/news_supporters_ids.tab', 'w') as f:
    f.write(news_supporters)

print("Done")
