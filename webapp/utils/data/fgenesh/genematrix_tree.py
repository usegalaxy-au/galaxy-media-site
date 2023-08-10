"""Render the JSON taxonomy tree as an HTML list."""

import json
from pathlib import Path

tree_path = Path(__file__).parent / 'genematrix_taxonomy_m.json'


def get_input_val(key, parent_key):
    return f"{parent_key}-{key.replace(' ', '-')}"


def as_choices():
    """Return a list of all input IDs available in the tree."""
    def get_items(node, parent_key):
        items = []
        if 'desc' in node:
            value = get_input_val(parent_key, parent_key)
            choice = (value, value)
            items.append(choice)
        for k, v in node.items():
            if k == 'desc':
                continue
            items.extend(get_items(v, k))
        return items

    with open(tree_path, 'r') as f:
        taxonomy_tree = json.load(f)

    items = []
    for k, v in taxonomy_tree.items():
        items.extend(get_items(v, k))

    if len(set(items) != len(items)):
        raise ValueError("Duplicate indexes found in tree.")

    return items


def as_ul():
    def render_li(node, key, parent_key, indent):
        def is_leaf(obj):
            if not isinstance(obj, dict):
                return True
            if set(obj.keys()) - {'desc'}:
                return False
            return True

        def sorted_keys(node):
            """Sort keys, putting those with 'desc' in value last."""
            def get_order(v):
                if isinstance(v, str):
                    return 3
                if 'desc' in v:
                    if {'desc'} == set(v.keys()):
                        return 2
                    return 1
                return 0
            keys = sorted(node.keys())
            keys.sort(key=lambda k: get_order(node[k]))
            return keys

        if key == 'desc':
            return ""

        if node:
            li = f'{"  " * indent}<li>\n'
            indent_str = "  " * (indent + 1)
            if 'desc' in node:
                # Create li with checkbox
                input_val = get_input_val(key, parent_key)
                checkbox = (f'{indent_str}<input type="checkbox"'
                            f' name="matrices" value="{input_val}"'
                            f' id="{input_val}">')
                if is_leaf(node):
                    li += f'{indent_str}<span class="choice">'
                else:
                    li += f'{indent_str}<span class="caret choice">'
                li += checkbox
                li += f'<label for="{input_val}">'
                li += f'{key} - {node["desc"]}'
                li += '</label>'
                li += '</span>\n'
            else:
                # Create li with caret and ul
                li += f'{indent_str}<span class="caret">{key}</span>\n'
            if not is_leaf(node):
                ul = f'{indent_str}<ul class="nested">\n'
                for k in sorted_keys(node):
                    v = node[k]
                    ul += render_li(v, k, key, indent + 2)
                ul += f'{indent_str}</ul>\n'
                li += ul
            li += f'{"  " * indent}</li>\n'
            return li

        return ""

    with open(tree_path, 'r') as f:
        taxonomy_tree = json.load(f)

    ul = '<ul id="taxonomy-tree" class="tree-select">\n'
    for k, v in taxonomy_tree.items():
        ul += render_li(v, k, 'root', 0)
    ul += '</ul>\n'

    return ul


if __name__ == '__main__':
    # Test peek at HTML output
    LINES = 50
    html = as_ul()
    for i, line in enumerate(html.split('\n')):
        if i > LINES:
            break
        print(line)
