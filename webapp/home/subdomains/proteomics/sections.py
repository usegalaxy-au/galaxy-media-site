"""Content for landing page is modularize in Python code and imported from this
file.
"""

from . import content

tools_heading_html = """Some example tools are listed here: you can also search for more in the full tool panel to the left."""

sections = [
    {
        "id": "database",
        "title": "Database searching",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.database_searching.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.database_searching.help,
            },
        ],
    },
    {
        "id": "dda_standardised_tools",
        "title": "Data dependent acquisition (DDA) standardised tools",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.dda_standardised_tools.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.dda_standardised_tools.help,
            },
        ],
    },
    {
        "id": "dia_standardised_tools",
        "title": "Data independent acquisition (DIA) standardised tools",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.dia_standardised_tools.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.dia_standardised_tools.help,
            },
        ],
    },
    {
        "id": "dda_tmt",
        "title": "DDA tandem mass tags (TMT)",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.dda_tmt.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.dda_tmt.help,
            },
        ],
    }
]
