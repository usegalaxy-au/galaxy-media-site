"""Content for data section - tools, workflows and help tabs."""

galaxy_au_support_item = {
    "title_md": 'Galaxy Australia support',
    "description_md": """<p>
            Any user of Galaxy Australia can request support through an
            online form.
        </p>""",
    "button_link": "/request/support",
    "button_md": "Request support",
}

tools = [
    # {   # Accordion item schema:
    #     "title_md": '',
    #     "description_md": """""",
    #     "inputs": [
    #         {
    #             'datatypes': [''],
    #             'label': '',
    #         },
    #     ],
    #     "button_link": "",
    #     "button_md": "",
    #     "button_tip": "",
    #     "view_link": "",
    #     "view_md": "",
    #     "view_tip": "",
    # },
    {
        "title_md": '<code>MSstats</code>',
        "description_md": '<p>Statistical relative protein significance analysis in DDA, SRM and DIA Mass Spectrometry.</p>',
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
