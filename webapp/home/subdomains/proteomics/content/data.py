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
        "title_md": "Import data to Galaxy",
        "description_md": "<p>Standard upload of data to Galaxy, from your computer or from the web.</p>",
        "button_link": '{{ galaxy_base_url }}/tool_runner?tool_id=upload1',
    }
]


help = [
    {
        "title_md": 'Can I upload sensitive data?',
        "description_md": """
            <p>
              No, do not upload personal or sensitive, such as human health or clinical data.
              Please see our
              <a href="/about#data-privacy">Data Privacy</a>
              page for definitions of sensitive and health-related information.
            </p>
            <p>
              Please also make sure you have read our
              <a href="/about#terms-of-service">Terms of Service</a>,
              which covers hosting and analysis of research data.
            </p>""",
    },
    {
        "title_md": 'Is my data private?',
        "description_md": """
            <p>
              Please read our
              <a href="/about#data-privacy">Privacy Policy</a>
              for information on your personal data and any data that you upload.
            </p>""",
    },
    {
        "title_md": 'How can I increase my storage quota?',
        "description_md": """
            <p>
                Please submit a quota request if your Galaxy Australia account reaches its data storage limit. Requests are usually provisioned quickly if you provide a reasonable use case for your request.
            </p>""",
        "button_link": "/request/quota",
        "button_md": "Request",
    },
    {
        "title_md": 'Tutorial: Introduction to proteomics, protein identification, quantification and statistical modelling',
        "description_md": """
            <p>
              This practical aims to familiarize you with Galaxy for Proteomics, including theory, methods and software examples.
            </p>""",
        "button_link": "https://training.galaxyproject.org/training-material/topics/proteomics/tutorials/introduction/slides.html#1",
        "button_md": "Tutorial",
    },
    galaxy_au_support_item,
]
