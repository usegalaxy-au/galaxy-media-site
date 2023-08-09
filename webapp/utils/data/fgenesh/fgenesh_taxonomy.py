"""Annotate FGENESH gene matrix with taxonomy information.

Queries the GBIF species API for taxonomic data.
"""

import json
import requests
import genematrix
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

ROOT = Path(__file__).parent
outfile = ROOT / 'genematrix_taxonomy.json'
missing_debug_file = ROOT / 'missing_debug.txt'
missing_response_file = ROOT / 'missing_response.json'
rank_debug_file = ROOT / 'rank_mismatch_debug.json'
missing_responses = {}


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
        try:
            response = requests.get(url, timeout=5)
            self.data = json.loads(response.text)
        except requests.ReadTimeout:
            self.data = None


def annotate():
    """Annotate gene matrix with taxonomic information."""
    def set_taxon_tree(taxa, species, desc):
        """Traverse dict to add current species taxonomy levels."""
        branch = taxa
        if TAXONOMY_LEVELS[0] not in species.data:
            raise KeyError("No taxonomic data found")
        for level in TAXONOMY_LEVELS:
            if level not in species.data:
                break
            taxon = species.data[level]
            if taxon not in branch:
                branch[taxon] = {}
            branch = branch[taxon]
        branch['desc'] = desc
        return taxa

    taxa = {}
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
            taxa = set_taxon_tree(taxa, species, desc)
        except KeyError:
            warn(f"No taxonomic data found for {name}")
            missing.append(name)
            missing_responses[name] = species.data
            continue

    if missing:
        with open(missing_debug_file, 'w') as f:
            f.write('\n'.join(missing))
    if rank_mismatch:
        with open(rank_debug_file, 'w') as f:
            json.dump(rank_mismatch, f, indent=2)
    if missing_responses:
        with open(missing_response_file, 'a') as f:
            json.dump(missing_responses, f, indent=2)

    success(f"\nCompleted with {len(missing)} missing and"
            f" {len(rank_mismatch)} mismatching records")
    print("\nTaxon rank counts:")
    for rank in TAXONOMY_LEVELS:
        print(f"{rank.title()}: {rank_count[rank]}")

    print(f"\nWriting to file {outfile}...")
    with open(outfile, 'w') as f:
        json.dump(taxa, f, indent=2)


if __name__ == '__main__':
    annotate()
