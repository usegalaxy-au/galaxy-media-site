"""Notifications to users and team.

This is some very Galaxy-Australia-specific code for event-bound notifications.
"""

import logging
import requests
from urllib.parse import urljoin
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger('django')


def notify_tool_update(article):
    """Send a notification to the team of posted tool updates/installs."""
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
    notify_slack(body)
    notify_emails(body)


def notify_slack(message):
    """Send a message to the team Slack channel."""
    if not settings.SLACK_API_URLS:
        logger.warning("No Slack API URL configured for notifications.")
        return
    requests.post(
        url=settings.SLACK_API_URLS,
        json={"text": message},
    )


def notify_emails(message):
    """Send a message to the team email addresses."""
    if not settings.TOOL_UPDATE_EMAILS:
        logger.warning("No email addresses configured for notifications.")
        return
    logger.info(
        "Sending tool update notification emails to:"
        f" {settings.TOOL_UPDATE_EMAILS}...")
    send_mail(
        "Galaxy Australia tool updates",
        message,
        settings.EMAIL_FROM_ADDRESS,
        settings.TOOL_UPDATE_EMAILS,
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
