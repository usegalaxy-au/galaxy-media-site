"""Parse scientific name and description from GeneMatrix table."""

import re
from pathlib import Path

PATH = Path(__file__).parent / 'genematrix.txt'


def get_input_val(key, desc):
    def clean(s):
        ss = re.sub(r'[^A-z0-9]', '-', s)
        return re.sub(r'-+', '-', ss)

    return f"{clean(key)}-{clean(desc)}"


def clean_desc(line):
    """Remove parentheses and whitespace from description."""
    match = re.findall(r'\([^\)]+\)', line)
    return '; '.join([m.strip(' ()') for m in match])


def get_matrices():
    """Return a list of dicts with matrix name and description."""
    matrices = []

    with open(PATH, 'r') as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            name = line.split('(')[0].strip()
            desc = clean_desc(line)
            matrices.append({'name': name, 'desc': desc})
    print(f"Parsed {len(matrices)} matrices.\n")
    return matrices
