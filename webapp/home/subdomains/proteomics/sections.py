"""Content for landing page is modularize in Python code and imported from this
file.
"""

from . import content

tools_heading_html = """Some example tools are listed here: you can also search for more in the full tool panel to the left."""

sections = [
    {
        "id": "data",
        "title": "Data import",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.data.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.data.help,
            },
        ],
    },
    {
        "id": "quant_proteomics",
        "title": "Quantitative proteomics",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.quant_proteomics.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.quant_proteomics.help,
            },
        ],
    },
    {
        "id": "post_processing_visualisation",
        "title": "Post processing and visualisation",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_html": tools_heading_html,
                "content": content.post_processing_visualisation.tools,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.post_processing_visualisation.help,
            },
        ],
    }
]
