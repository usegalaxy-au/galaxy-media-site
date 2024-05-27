"""Run this script when updating institutions.json"""

import json
from pathlib import Path

parent = Path(__file__).resolve().parent
INSTITUTIONS_JSON = parent / 'institutions.json'
DOMAINS_JSON = parent / 'domains.json'


def main():
    with open(INSTITUTIONS_JSON) as f:
        institutions = json.load(f)

    domains = {}
    for institution in institutions:
        for domain in institution['domains']:
            domains[domain] = institution['name']

    with open(DOMAINS_JSON, 'w') as f:
        json.dump(domains, f, indent=2)

    print(f"\nRegenerated {DOMAINS_JSON}")


if __name__ == '__main__':
    main()
