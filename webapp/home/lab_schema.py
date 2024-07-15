"""Schema for validating Galaxy Lab content."""

from enum import Enum
from pydantic import BaseModel
from typing import Optional, Union


class IconEnum(str, Enum):
    """Define material icon types for buttons."""
    run = 'run'            # play_arrow
    tutorial = 'tutorial'  # school
    social = 'social'      # group
    help = 'help'          # help


class TabContentEnum(str, Enum):
    """Define the type of content in a tab item."""
    subsections = 'subsections'


class TabItem(BaseModel):
    """Validate Galaxy Lab section tab item.

    In the UI this will be rendered as an "accordion" item.
    """
    title_md: str
    description_md: str
    button_link: Optional[str] = None
    button_tip: Optional[str] = None
    button_html: Optional[str] = None
    button_icon: Optional[IconEnum] = None
    view_link: Optional[str] = None
    view_tip: Optional[str] = None
    view_html: Optional[str] = None
    view_icon: Optional[str] = None
    exclude_from: Optional[list[str]] = []


class TabSubsection(BaseModel):
    """Validate Galaxy Lab section tab subsection."""
    id: str
    title: str
    content: list[TabItem]


class SectionTab(BaseModel):
    """Validate Galaxy Lab section tab."""
    id: str
    title: Optional[str] = None
    content: Optional[
        Union[
            list[TabItem],
            dict[TabContentEnum, list[TabSubsection]]
        ]
    ] = None
    heading_md: Optional[str] = None


class LabSectionSchema(BaseModel):
    """Validate Galaxy Lab section."""
    id: str
    tabs: list[SectionTab]


class LabSchema(BaseModel):
    """Validate Galaxy Lab content."""
    site_name: str
    lab_name: str
    nationality: str
    galaxy_base_url: str
    subdomain: str
    root_domain: str
    sections: list[str] | str
    header_logo: Optional[str] = None
    custom_css: Optional[str] = None
    intro_md: Optional[str] = None
    conclusion_md: Optional[str] = None
    footer_md: Optional[str] = None
    intro_md: Optional[str] = None
    conclusion_md: Optional[str] = None
    footer_md: Optional[str] = None
