"""Recursive merge a pair of dictionaries."""

from copy import deepcopy


def recursive_merge(x, y):
    """Perform recursive merge of dictionaries."""
    if not (type(x) == dict and type(y) == dict):
        if not (type(x) == dict or type(y) == dict):
            return
        if not type(x) == dict:
            return y
        if not type(y) == dict:
            return x
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = recursive_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z
