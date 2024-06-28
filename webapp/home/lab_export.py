"""Exported landing pages to be requested by external Galaxy servers.

Example with local YAML:
http://127.0.0.1:8000/landing/export?content_root=http://127.0.0.1:8000/static/home/labs/genome/main.yml

Example URL with remote YAML:
http://127.0.0.1:8000/landing/export?content_root=https://raw.githubusercontent.com/usegalaxy-au/galaxy-media-site/dev/webapp/home/static/home/labs/genome/main.yml

"""

import logging
import requests
import yaml
from pydantic import ValidationError

from types import SimpleNamespace
from utils.exceptions import SubsiteBuildError
from .lab_schema import LabSchema, LabSectionSchema

logger = logging.getLogger('django')

ACCEPTED_IMG_EXTENSIONS = ('png', 'jpg', 'jpeg', 'svg', 'webp')

CONTENT_TYPES = SimpleNamespace(
    WEBPAGE='webpage',
    YAML='yaml',
)


class ExportSubsiteContext(dict):
    """Build and validate render context for exported subsite landing page.

    These page are intended to be displayed externally to the host Galaxy
    (i.e. on a different Galaxy server).

    The context can be built from GET params or from an externally hosted YAML
    context specified by a ``content_root`` GET param.
    """

    HTML_SNIPPETS = (
        'intro_html',
        'header_logo',
        'footer_html',
        'conclusion_html',
        'custom_css',
    )

    def __init__(self, content_root):
        """Init context from dict."""
        super().__init__(self)
        self['snippets'] = {}
        self.content_root = content_root
        self.update({
            'export': True,
            'extend_template': 'home/header-export.html',
        })
        self._fetch_yaml_context()
        self._fetch_sections()

    def _clean(self):
        """Format params for rendering."""
        self['galaxy_base_url'].strip('/')

    def validate(self):
        """Validate against required params."""
        self._validate_sections()
        self._clean()

    def _validate_sections(self):
        """Validate sections against Pydantic schema."""
        for section in self['sections']:
            try:
                LabSectionSchema(**section)
            except ValidationError as e:
                raise SubsiteBuildError(
                    e,
                    section_id=section["id"],
                    source='YAML',
                )

    def _get(self, url, expected_type=None):
        """Fetch content from URL and validate returned content."""
        res = requests.get(self._make_raw(url))
        if res.status_code >= 300:
            raise SubsiteBuildError(
                f'HTTP {res.status_code} fetching file.',
                url=url)
        if expected_type != CONTENT_TYPES.WEBPAGE:
            lines = [
                x.strip()
                for x in res.content.decode('utf-8').split('\n')
                if x.strip()
            ]
            if lines and '<!doctype html>' in lines[0].lower():
                expected = expected_type or 'a raw file'
                raise SubsiteBuildError(
                    (
                        "Unexpected HTML content in file.\n"
                        'The URL provided returned a webpage (HTML) when'
                        f' {expected} was expected.'
                    ),
                    url=url,
                    source='YAML',
                )
        return res

    def _make_raw(self, url):
        """Make raw URL for fetching content."""
        if 'github.com' in url:
            url = (
                url.replace('github.com', 'raw.githubusercontent.com')
                .replace('/blob/', '/'))
        return url

    def _fetch_yaml_context(self):
        """Fetch params from remote YAML file.

        This file is typically named main.yml.
        """
        if not self.content_root:
            raise ValueError(
                "GET parameter 'content_root' required for root URL")
        res = self._get(self.content_root, expected_type=CONTENT_TYPES.YAML)
        yaml_str = res.content.decode('utf-8')
        try:
            params = yaml.safe_load(yaml_str)
        except (yaml.YAMLError, yaml.scanner.ScannerError) as exc:
            raise SubsiteBuildError(exc, url=self.content_root, source='YAML')
        try:
            LabSchema(**params)
        except ValidationError as exc:
            raise SubsiteBuildError(exc, url=self.content_root, source='YAML')
        self.update(params)
        self._fetch_snippets()

    def _fetch_sections(self):
        """Fetch webpage sections content from remote YAML file."""
        sections = self.get('sections')
        if isinstance(sections, str):
            self['sections'] = self._fetch_yaml_content(self.get('sections'))
        elif isinstance(sections, list):
            self['sections'] = [
                self._fetch_yaml_content(s)
                for s in sections
            ]
        return sections

    def _fetch_yaml_content(self, relpath):
        """Recursively fetch web content from remote YAML file."""
        yaml_url = self.content_root
        if not (yaml_url and relpath):
            return
        if relpath.startswith('http'):
            url = relpath
        else:
            url = yaml_url.rsplit('/', 1)[0] + '/' + relpath.lstrip('./')
        res = self._get(url, expected_type=CONTENT_TYPES.YAML)
        yaml_str = res.content.decode('utf-8')

        try:
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError as exc:
            raise SubsiteBuildError(exc, url=url)

        if isinstance(data, dict):
            data = {
                # Fetch remote YAML if value is <str>.yml
                k: self._fetch_yaml_content(v) or v
                if isinstance(v, str) and v.split('.')[-1] in ('yml', 'yaml')
                else v
                for k, v in data.items()
            }

        return data

    def _fetch_snippets(self):
        """Fetch HTML snippets and add to context.snippets."""
        for name in self.HTML_SNIPPETS:
            if relpath := self.get(name):
                if relpath.rsplit('.', 1)[1] in ACCEPTED_IMG_EXTENSIONS:
                    self['snippets'][name] = self._fetch_img_src(relpath)
                else:
                    self['snippets'][name] = self._fetch_snippet(relpath)

    def _fetch_img_src(self, relpath):
        """Build URL for image."""
        if self.content_root:
            return (self.content_root.rsplit('/', 1)[0]
                    + '/' + relpath.lstrip('./'))

    def _fetch_snippet(self, relpath):
        """Fetch HTML snippet from remote URL."""
        if self.content_root:
            url = (self.content_root.rsplit('/', 1)[0]
                   + '/' + relpath.lstrip('./'))
            res = self._get(url)
            return res.content.decode('utf-8')
