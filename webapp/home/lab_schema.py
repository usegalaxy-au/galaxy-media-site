"""Schema for validating Galaxy Lab content."""

from pydantic import BaseModel
from typing import Optional, Union


class TabItem(BaseModel):
    """Validate Galaxy Lab section tab item.

    In the UI this will be rendered as an "accordion" item.
    """
    title_html: str
    description_html: str
    button_link: Optional[str] = None
    button_tip: Optional[str] = None
    view_link: Optional[str] = None
    view_tip: Optional[str] = None


class TabSubsection(BaseModel):
    """Validate Galaxy Lab section tab subsection."""
    id: str
    title: str
    content: list[TabItem]


class SectionTab(BaseModel):
    """Validate Galaxy Lab section tab."""
    id: str
    title: str
    content: Union[list[TabItem], dict[str, list[TabSubsection]]]


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
    intro_html: Optional[str] = None
    conclusion_html: Optional[str] = None
    footer_html: Optional[str] = None
    au_include_header_cards: Optional[bool] = False
