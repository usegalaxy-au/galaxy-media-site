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
        "title_md": '<code>DecoyDatabase</code>',
        "description_md": '<p>Create decoy sequence database from forward sequence database.</p>',
        "inputs": [
            {
                'datatypes': ['fasta'],
                'label': 'Input FASTA file(s), each containing a database',
            }
        ],
        "button_link": "{{ galaxy_base_url }}/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/openms_decoydatabase/DecoyDatabase/",
    },
    {
        "title_md": '<code>MaxQuant</code>',
        "description_md": '<p>MaxQuant is a quantitative proteomics software package designed for analyzing large mass-spectrometric data sets.</p>',
        "inputs": [
            {
                'datatypes': ['thermo.raw', 'mzML', 'mzXML'],
                'label': 'Mass spectrometry data sets'
            },
            {
                'datatypes': ['tabular'],
                'label': 'Experimental design template',
            },
        ],
        "button_link": "{{ galaxy_base_url }}/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/maxquant/maxquant/",
    },
    {
        "title_md": '<code>Morpheus</code>',
        "description_md": '<p>Database search algorithm for high-resolution tandem mass spectra.</p>',
        "inputs": [
            {
                'datatypes': ['mzML'],
                'label': 'Indexed mzML',
            },
            {
                'datatypes': ['fasta', 'uniprotxml'],
                'label': 'MS Protein Search Database: UniProt Xml or Fasta',
            },
        ],
        "button_link": "https://proteomics.usegalaxy.org.au/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/morpheus/morpheus/",
    }
]

help = []  # Todo
