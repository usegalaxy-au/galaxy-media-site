"""Annotate FGENESH gene matrix with taxonomy information.

Queries the GBIF species API for taxonomic data.

TODO: There are issues with the GBIF API - posted issues:

- https://github.com/gbif/portal-feedback/issues/4906
- https://github.com/gbif/portal-feedback/issues/4907

- Currently the Reptilia and Actinopterygii are not being annotated correctly,
  resulting in most records being lost.
- Gobiidae, Sciaenidae, Cichlidae wrongly allocated to order Perciformes.

The above have been fixed with the taxonomy_patch module.

"""

import json
import requests
import genematrix
import taxonomy_patch
from pathlib import Path
from collections import Counter

TAXONOMY_LEVELS = [
    'kingdom',
    'phylum',
    'class',
    'order',
    'family',
    'genus',
    'species',
]

ROOT = Path(__file__).parent / 'outputs'
OUTFILE = ROOT / 'genematrix_taxonomy.json'
MISSING_DEBUG_FILE = ROOT / 'missing_debug.txt'
MISSING_RESPONSE_FILE = ROOT / 'missing_response.json'
RANK_DEBUG_FILE = ROOT / 'rank_mismatch_debug.json'
DUPLICATES_ENTRIES_FILE = ROOT / 'duplicates_entries.json'
MISSING_CLASS_FILE = ROOT / "missing_classes.json"

missing_responses = {}
duplicate_entries = {}

for f in [MISSING_CLASS_FILE, MISSING_RESPONSE_FILE, DUPLICATES_ENTRIES_FILE]:
    if f.exists():
        f.unlink()


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def success(msg):
    print(f"{BColors.OKGREEN}{msg}{BColors.END}")


def warn(msg):
    print(f"{BColors.WARNING}{msg}{BColors.END}")


class SpeciesSearch:
    """Query the species API with supplied species name.

    Send a query string to the GBIF species API and parse the returned
    json dict into the data attribute. This field makes taxon information
    accessible as dict keys such as kingdom, phylum, class, order, family,
    genus.

    Available keys in obj.data:
    ---------------------------
    - kingdom
    - phylum
    - order
    - family
    - genus
    - species
    - rank

    """

    def __init__(self, query):
        url = ('https://api.gbif.org/v1/species/match?'
               f'name={query}')
        self.query = query
        try:
            response = requests.get(url, timeout=5)
            self.data = json.loads(response.text)
        except requests.ReadTimeout:
            self.data = None
            return

        if not self.data.get('class'):
            with open(MISSING_CLASS_FILE, 'a') as f:
                json.dump({query: self.data}, f, indent=2)

        self.data = taxonomy_patch.reptilia(self.data)
        self.data = taxonomy_patch.fish(self.data)
        self.data = taxonomy_patch.perciformes(self.data)
        self.data = taxonomy_patch.missing(self.data, query)


def annotate():
    """Annotate gene matrix with taxonomic information."""
    def set_taxon_tree(tree, species, desc):
        """Traverse dict to add current species taxonomy levels."""
        branch = tree
        if TAXONOMY_LEVELS[0] not in species.data:
            raise KeyError("No taxonomic data found")
        for level in TAXONOMY_LEVELS:
            if level not in species.data:
                break
            taxon = species.data[level]
            if taxon not in branch:
                branch[taxon] = {}
            branch = branch[taxon]
        if 'desc' in branch:
            key = f"{species.query}_{branch['desc']}"
            entry = {
                'name': taxon,
                'desc': desc,
                'data': species.data,
            }
            if key in duplicate_entries:
                duplicate_entries[key].append(entry)
            else:
                duplicate_entries[key] = [entry]

            branch['desc'].append(desc)
        else:
            branch['desc'] = [desc]
        return tree

    tree = {}
    rank_count = Counter()
    missing = []
    rank_mismatch = []
    matrices = genematrix.get_matrices()
    for ix, matrix in enumerate(matrices):
        name = matrix['name']
        desc = matrix['desc']
        print(f"{ix + 1}) Searching for {name}...")
        species = SpeciesSearch(name)
        if not species.data:
            warn(f"No record found for {name}")
            missing.append(name)
            continue
        try:
            rank = species.data['rank'].lower()
            success(f"Returned entry with rank: {rank}")
            rank_count[rank] += 1
            if rank not in TAXONOMY_LEVELS:
                warn(f"Rank {rank} not in taxonomy levels")
                rank_mismatch.append({'name': name, 'rank': rank})
                continue
            tree = set_taxon_tree(tree, species, desc)
        except KeyError:
            warn(f"No taxonomic data found for {name}")
            missing.append(name)
            missing_responses[name] = species.data
            continue

    if missing:
        with open(MISSING_DEBUG_FILE, 'w') as f:
            f.write('\n'.join(missing))
    if rank_mismatch:
        with open(RANK_DEBUG_FILE, 'w') as f:
            json.dump(rank_mismatch, f, indent=2)
    if missing_responses:
        with open(MISSING_RESPONSE_FILE, 'a') as f:
            json.dump(missing_responses, f, indent=2)

    with open(DUPLICATES_ENTRIES_FILE, 'a') as f:
        json.dump(duplicate_entries, f, indent=2)

    success(f"\nCompleted with:\n"
            f"  {len(missing)} missing\n"
            f"  {len(rank_mismatch)} mismatching\n"
            f"  {len(duplicate_entries)} duplicate entries")

    print("\nTaxon rank counts:")
    for rank in TAXONOMY_LEVELS:
        print(f"{rank.title()}: {rank_count[rank]}")

    print(f"\nWriting to file {OUTFILE}...")
    with open(OUTFILE, 'w') as f:
        json.dump(tree, f, indent=2)


if __name__ == '__main__':
    annotate()
