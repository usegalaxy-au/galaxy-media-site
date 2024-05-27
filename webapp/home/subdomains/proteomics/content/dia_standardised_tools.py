"""Content for data section - tools, workflows and help tabs."""

galaxy_au_support_item = {
    "title_html": 'Galaxy Australia support',
    "description_html": """<p>
            Any user of Galaxy Australia can request support through an
            online form.
        </p>""",
    "button_link": "/request/support",
    "button_html": "Request support",
}

tools = [
    # {   # Accordion item schema:
    #     "title_html": '',
    #     "description_html": """""",
    #     "inputs": [
    #         {
    #             'datatypes': [''],
    #             'label': '',
    #         },
    #     ],
    #     "button_link": "",
    #     "button_html": "",
    #     "button_tip": "",
    #     "view_link": "",
    #     "view_html": "",
    #     "view_tip": "",
    # },
    {
        "title_html": '<code>MSstats</code>',
        "description_html": '<p>Statistical relative protein significance analysis in DDA, SRM and DIA Mass Spectrometry.</p>',
        "inputs": [
            {
                'datatypes': ['tabular', 'csv'],
                'label': 'Either the 10-column MSstats format or the outputs of spectral processing tools such as MaxQuant, OpenSWATH.',
            }
        ],
        "button_link": "https://usegalaxy.org.au/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/msstats/msstats/",
    }
]


help = []
