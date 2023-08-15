"""Fix incorrect taxonomies resulting from errors in GBIF API."""

import json
from pathlib import Path

MISSING_DATA_FILE = Path(__file__).parent / "patch_missing_data.json"
TAXONOMY_LEVELS = [
    'kingdom',
    'phylum',
    'class',
    'order',
    'family',
    'genus',
    'species',
]
REPTILIA_ORDERS = ["Squamata", "Crocodylia", "Testudines", "Emydidae"]
ACTINOPTERYGII_ORDERS = [
    "Beloniformes",
    "Cichliformes",
    "Gobiiformes",
    "Perciformes",
    "Acanthuriformes",
    "Anguilliformes",
    "Scorpaeniformes",
    "Characiformes",
    "Cyprinodontiformes",
    "Clupeiformes",
    "Cypriniformes",
    "Pleuronectiformes",
    "Esociformes",
    "Gasterosteiformes",
    "Lepisosteiformes",
    "Salmoniformes",
    "Petromyzontiformes",
    "Tetraodontiformes",
]
CHONDRICHTHYES_ORDERS = [
    "Chimaeriformes",
]
PERCIFORMES_CORRECTION = {
    "Cichlidae": "Cichliformes",
    "Gobiidae": "Gobiiformes",
    "Sciaenidae": "Acanthuriformes",
}

with open(MISSING_DATA_FILE) as f:
    missing_data = json.load(f)


def reptilia(data):
    """Patch missing taxonomic data for Reptilia."""
    if (
        data.get('phylum') == 'Chordata'
        and data.get('class') in REPTILIA_ORDERS
    ):
        data['order'] = data['class']
        data['class'] = 'Reptilia'
    return data


def fish(data):
    """Patch missing taxonomic data for Actinopterygii."""
    if data.get('phylum') == 'Chordata':
        if data.get('order') in ACTINOPTERYGII_ORDERS:
            data['class'] = 'Actinopterygii'
        elif data.get('order') in CHONDRICHTHYES_ORDERS:
            data['class'] = 'Chondrichthyes'
    return data


def perciformes(data):
    """Patch taxa incorrectly assigned to order Perciformes."""
    if data.get('family') in PERCIFORMES_CORRECTION:
        data['order'] = PERCIFORMES_CORRECTION[data['family']]
    return data


def missing(data, query):
    if data["matchType"] == "NONE" and query in missing_data:
        matching_rank = None
        for rank in TAXONOMY_LEVELS:
            if rank not in missing_data[query]:
                break
            matching_rank = rank
            data[rank] = missing_data[query][rank]
        if matching_rank:
            data['rank'] = matching_rank
    return data


if __name__ == '__main__':
    print('Fill in missing data for Babesia:')
    data = missing({'matchType': 'NONE'}, 'Babesia')
    print(data)
