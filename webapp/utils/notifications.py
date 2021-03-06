"""Notifications to users and team.

This is some very Galaxy-Australia-specific code for event-bound notifications.
"""

import requests
from urllib.parse import urljoin
from django.conf import settings


def notify_tool_update(article):
    """Send a notification to the team of posted tool updates/installs."""
    if not settings.SLACK_API_URL:
        return
    updates = parse_tool_updates(article.body)

    body = (
        "*New tool updates on Galaxy Australia*:\n"
        + urljoin(f'http://{settings.HOSTNAME}', f"/news/{article.id}")
    )
    if updates['installed']:
        body += "\n\n*Installed:*\n"
        body += '\n'.join([
            f"{x[0]}: {x[1].strip('()')}" for x in updates['installed']
        ])
    if updates['updated']:
        body += "\n\n*Updated:*\n"
        body += '\n'.join([
            f"{x[0]}: {x[1].strip('()')}" for x in updates['updated']
        ])

    requests.post(
        url=settings.SLACK_API_URL,
        json={"text": body},
    )


def parse_tool_updates(markdown):
    """Parse tool updates from news article markdown."""
    updates = {
        'installed': [],
        'updated': [],
    }

    if "### Tools installed" in markdown:
        installed_lines = (
            markdown.split('### Tools installed')[1]
            .split('###')[0]
            .split('\n')
        )
        updates['installed'] = get_tools_list(installed_lines)

    if "### Tools updated" in markdown:
        updated_lines = markdown.split('### Tools updated')[1].split('\n')
        updates['updated'] = get_tools_list(updated_lines)

    return updates


def get_tools_list(lines):
    """Parse tools list from tool update markdown table lines."""
    tools = []
    for line in lines:
        if line.startswith('| **'):
            # It's an installed section line. Parse a tool list from it.
            tools += [
                (
                    x.split('[')[0].strip(),      # name
                    convert_toolshed_id_url(
                        x.split(']')[1].strip('()')
                    ),  # galaxy toolshed url id
                ) for x in line.split('|')[2].split('<br/>')
            ]
    return tools


def convert_toolshed_id_url(url):
    """Convert a toolshed webpage URL to tool identifier URL."""
    parts = url.split('//')[1].split('/')
    tool_id = parts[-2]
    new = '/'.join(parts[:-1] + [tool_id])
    return new.replace('view', 'repos')
