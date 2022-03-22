"""Slack notifications for log handling."""

import os
import requests

SLACK_URL = "https://slack.com/api/chat.postMessage"

FILTER_PHRASES = [
    'invalid http_host header',
]


def is_excluded_message(message):
    """Determine whether message should be excluded from Slack."""
    for phrase in FILTER_PHRASES:
        if phrase in message.lower():
            return True


def post(message=None, channel_id=None, user_id=None, key=None):
    """Post a message to Slack."""
    if is_excluded_message(message):
        return
    key = os.environ.get("SLACK_API_KEY")
    user_id = os.environ.get("SLACK_MENTION_USER_ID")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")

    if key is None:
        return
    if user_id:
        message = f'<@{user_id}> {message}'

    requests.post(
        SLACK_URL,
        json={
            "text": message,
            "channel": channel_id,
        },
        headers={
            "Authorization": f'Bearer {key}',
        },
    )
