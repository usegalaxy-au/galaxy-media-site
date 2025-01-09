"""Render the JSON taxonomy tree as an HTML list."""

import json
from pathlib import Path
from .fetch_taxonomies.genematrix import get_input_val

# Manually curated:
# tree_path = Path(__file__).parent / 'genematrix_taxonomy_curated.json'

# Programatically curated:
tree_path = Path(__file__).parent / 'genematrix_taxonomy.json'


def as_choices():
    """Return a list of all input IDs available in the tree."""
    def get_items(key, node):
        items = []
        if 'desc' in node:
            for desc in node['desc']:
                value = get_input_val(key, desc)
                choice = (value, value)
                items.append(choice)
        for k, v in node.items():
            if k == 'desc':
                continue
            items.extend(get_items(k, v))
        return items

    with open(tree_path, 'r') as f:
        taxonomy_tree = json.load(f)

    items = []
    for k, v in taxonomy_tree.items():
        items.extend(get_items(k, v))

    if len(set(items)) != len(items):
        duplicates = [x for x in items if items.count(x) > 1]
        raise ValueError(
            f"Duplicate indexes found in tree: {duplicates}\n"
            "Please check the FGENESH GeneMatrix taxonomy tree for this"
            f" duplicate key: {tree_path}")

    return items


def as_ul():
    def render_li(node, key, indent):
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

        def render_leaf_li(key, desc, checkbox=False):
            """Render a list item representing a matrix choice."""
            tag = f'{"  " * indent}<li>\n'
            indent_str = "  " * (indent + 1)
            input_val = get_input_val(key, desc)
            checkbox_html = (
                f'{indent_str}<input type="checkbox"'
                f' name="matrices" value="{input_val}"'
                f' id="{input_val}">'
            )
            if not checkbox:
                icon = '<i class="fas fa-check-square" style="color: limegreen;"></i>'
                checkbox_html = icon + checkbox_html.replace(
                    'type="checkbox"', 'type="hidden"')
            text = key
            if desc:
                text += f' - {desc}'
            return (
                f'{tag}{indent_str}<span class="choice">'
                f'{checkbox_html}'
                f'<label for="{input_val}">'
                f"{text}"
                '</label>'
                '</span>\n'
            )

        if key == 'desc':
            return ""

        if not node:
            return ""

        if is_leaf(node):
            # Create a <li> for each [desc]
            lis = []
            for desc in node['desc']:
                li = render_leaf_li(key, desc)
                lis.append(li)
            return "\n".join(lis)

        # Else, create branch with caret and ul
        li = f'{"  " * indent}<li>\n'
        indent_str = "  " * (indent + 1)
        li += f'{indent_str}<span class="caret">{key}</span>\n'
        ul = f'{indent_str}<ul class="nested">\n'
        for k in sorted_keys(node):
            v = node[k]
            ul += render_li(v, k, indent + 2)
        if 'desc' in node:
            # for each desc[] add leaf to branch
            for desc in node['desc']:
                ul += render_leaf_li(key, desc)
        ul += f'{indent_str}</ul>\n'
        li += ul
        li += f'{"  " * indent}</li>\n'
        return li

    with open(tree_path, 'r') as f:
        taxonomy_tree = json.load(f)

    ul = '<ul id="taxonomy-tree" class="tree-select">\n'
    for k, v in taxonomy_tree.items():
        ul += render_li(v, k, 0)
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
