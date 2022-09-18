"""Parse HTML email addresses to JSON."""

import json

SRC = (
    "/home/cameron/dev/galaxy/galaxy-content-site"
    "/webapp/home/templates/home/snippets/about/list-of-institutions.html"
)
OUTFILE = "email_list.json"

with open(SRC) as f:
    lines = [
        line for line in f.read().split('\n')
        if "<td>" in line
    ]

addresses = {
    # name: [ domain, domain, ... ]
}

for line in lines:
    if "@" not in line:
        name = line.split('>')[1].split('<')[0].strip()
    else:
        address_list = [
            x.strip()
            for x in (
                line.split('>')[1]
                .split('<')[0]
                .strip()
                .split(',')
            )
        ]
        for a in address_list:
            addresses[a] = name

with open(OUTFILE, 'w') as f:
    json.dump(addresses, f, indent=4)
