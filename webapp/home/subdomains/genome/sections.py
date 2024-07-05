"""Content for landing page is modularize in Python code and imported from this
file.
"""

from . import content

workflow_heading_md = """A workflow is a series of Galaxy tools that have been linked together to perform a specific analysis. You can use and customize the example workflows below.
<a href="https://galaxyproject.org/learn/advanced-workflow/" target="_blank">Learn more.</a>
"""

tools_heading_md = """Common tools are listed here, or search for more in the full tool panel to the left."""

sections = [
    {
        "id": "data",
        "title": "Data import and preparation",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_md": tools_heading_md,
                "content": content.data.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_md": workflow_heading_md,
                "content": content.data.workflows,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.data.help,
            },
        ],
    },
    {
        "id": "assembly",
        "title": "Genome assembly",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_md": tools_heading_md,
                "content": content.assembly.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_md": workflow_heading_md,
                "content": content.assembly.workflows,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.assembly.help,
            },
        ],
    },
    {
        "id": "annotation",
        "title": "Genome annotation",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "heading_md": tools_heading_md,
                "content": content.annotation.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_md": workflow_heading_md,
                "content": content.annotation.workflows,
            },
            {
                "id": "help",
                "title": "Help",
                "content": content.annotation.help,
            },
        ],
    },
]
