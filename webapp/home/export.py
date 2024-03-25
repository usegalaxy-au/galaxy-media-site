"""Exported landing pages to be requested by external Galaxy servers.

Example URL:
http://127.0.0.1:8000/landing/genome?export=true&site_name=Australia&lab_name=Genome%20Lab&nationality=Antarctican&galaxy_base_url=http://mygalaxy.org

With remote YAML:
http://127.0.0.1:8000/landing/genome?export=true&content_root=https://raw.githubusercontent.com/usegalaxy-au/galaxy-media-site/export-lab-pages/webapp/home/test/data/subsite/media/subsite.yml
"""

import logging
import requests
import yaml
from django.core.exceptions import SuspiciousOperation

logger = logging.getLogger('django')


class ExportSubsiteContext(dict):
    """Build and validate render context for exported subsite landing page.

    These page are intended to be displayed externally to the host Galaxy
    (i.e. on a different Galaxy server).

    The context can be built from GET params or from an externally hosted YAML
    context specified by a ``content_root`` GET param.
    """

    REQUIRED_PARAMS = (
        #! TODO: this should be handled by Pydantic
        'site_name',
        'nationality',
        'galaxy_base_url',
    )
    HTML_SNIPPETS = (
        'intro_html',
        'header_logo',
        'footer_html',
        'custom_css',
    )

    def __init__(self, params):
        """Init context from dict."""
        super().__init__(self)
        self['snippets'] = {}
        self.params = params
        self.update({
            'export': True,
            'extend_template': 'home/header-export.html',
        })
        self._fetch_yaml_context()
        self._fetch_sections()

    def _clean(self):
        """Format params for rendering."""
        self['nationality'].capitalize()
        self['galaxy_base_url'].strip('/')

    def validate(self):
        """Validate against required params."""
        for k in self.REQUIRED_PARAMS:
            if not self.get(k):
                msg = f"GET parameter '{k}' is required for webpage export."
                logger.warning('Error validating exported subsite request:'
                               + msg)
                raise SuspiciousOperation(msg)
        self._clean()

    def _fetch_yaml_context(self):
        """Fetch params from remote YAML file."""
        url = self.params.get('content_root')
        if not url:
            raise ValueError("GET parameter 'content_root' required for root URL")
        yaml_str = requests.get(url).content.decode('utf-8')
        params = yaml.safe_load(yaml_str)
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
        """Fetch web content from remote YAML file if specified."""
        yaml_url = self.params.get('content_root')
        if not (yaml_url and relpath):
            return
        url = yaml_url.rsplit('/', 1)[0] + '/' + relpath.lstrip('./')
        response = requests.get(url)
        if response.status_code >= 300:
            raise SuspiciousOperation(
                f'HTTP {response.status_code} fetching file: {url}')
        yaml_str = response.content.decode('utf-8')
        data = yaml.safe_load(yaml_str)
        expanded = {
            k: self._fetch_yaml_content(v) or v
            if isinstance(v, str) and v.split('.')[-1] in ('yml', 'yaml')
            else v
            for k, v in data.items()
        }
        return expanded

    def _fetch_snippets(self):
        """Fetch HTML snippets and add to context.snippets."""
        for name in self.HTML_SNIPPETS:
            if relpath := self.get(name):
                if relpath.rsplit('.', 1)[1] in ('jpg', 'png', 'svg'):
                    self['snippets'][name] = self._fetch_img_src(relpath)
                else:
                    self['snippets'][name] = self._fetch_snippet(relpath)

    def _fetch_img_src(self, relpath):
        """Build URL for image."""
        yaml_url = self.params.get('content_root')
        if yaml_url:
            return yaml_url.rsplit('/', 1)[0] + '/' + relpath.lstrip('./')

    def _fetch_snippet(self, relpath):
        """Fetch HTML snippet from remote URL."""
        yaml_url = self.params.get('content_root')
        if yaml_url:
            url = yaml_url.rsplit('/', 1)[0] + '/' + relpath.lstrip('./')
            response = requests.get(url)
            if response.status_code >= 300:
                raise SuspiciousOperation(
                    f'HTTP {response.status_code} fetching file: {url}')
            return response.content.decode('utf-8')
