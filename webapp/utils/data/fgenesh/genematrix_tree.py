"""Render the JSON taxonomy tree as an HTML list."""

import json
from pathlib import Path

tree_path = Path(__file__).parent / 'genematrix_taxonomy_m.json'


def as_ul():
    def render_to_li(node, parent, indent):
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

        if parent == 'desc':
            return ""

        if node:
            li = f'{"  " * indent}<li>\n'
            indent_str = "  " * (indent + 1)
            if 'desc' in node:
                # Create li with checkbox
                input_id = f"{parent}-{parent.replace(' ', '-')}"
                checkbox = (f'{indent_str}<input type="checkbox"'
                            f' name="matrices" id="{input_id}">')
                if is_leaf(node):
                    li += f'{indent_str}<span">'
                else:
                    li += f'{indent_str}<span class="caret">'
                li += checkbox
                li += f'{parent} - {node["desc"]}'
                li += '</span>\n'
            else:
                # Create li with caret and ul
                li += f'{indent_str}<span class="caret">{parent}</span>\n'
            if not is_leaf(node):
                ul = f'{indent_str}<ul class="nested">\n'
                for k in sorted_keys(node):
                    v = node[k]
                    ul += render_to_li(v, k, indent + 2)
                ul += f'{indent_str}</ul>\n'
                li += ul
            li += f'{"  " * indent}</li>\n'
            return li

        return ""

    with open(tree_path, 'r') as f:
        taxonomy_tree = json.load(f)

    ul = '<ul id="taxonomy-tree" class="tree-select">\n'
    for k, v in taxonomy_tree.items():
        ul += render_to_li(v, k, 0)
    ul += '</ul>\n'

    return ul


if __name__ == '__main__':
    # Peek at HTML output
    LINES = 50
    html = as_ul()
    for i, line in enumerate(html.split('\n')):
        if i > LINES:
            break
        print(line)
