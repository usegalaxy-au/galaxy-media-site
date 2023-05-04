from . import content

workflow_heading_html = """A workflow is a series of Galaxy tools that have been linked together to perform a specific analysis. You can use and customize the example workflows below.
<a href="https://galaxyproject.org/learn/advanced-workflow/" target="_blank">Learn more.</a>
"""

sections = [
    {
        "id": "data",
        "title": "Data import and preparation",
        "tabs": [
            {
                "id": "tools",
                "title": "Tools",
                "content": content.data.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_html": workflow_heading_html,
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
                "content": content.assembly.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_html": workflow_heading_html,
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
                "content": content.annotation.tools,
            },
            {
                "id": "workflows",
                "title": "Workflows",
                "heading_html": workflow_heading_html,
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
