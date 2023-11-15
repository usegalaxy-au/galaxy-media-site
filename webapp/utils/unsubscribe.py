"""Functions for unsubscribing user from mail."""

from django.conf import settings


def add(user_hash):
    """Add hash to unsubscribe list file."""
    with open(settings.UNSUBSCRIBED_HASH_FILE) as f:
        if user_hash in f.read():
            return
    with open(settings.UNSUBSCRIBED_HASH_FILE, 'a') as f:
        f.write(f'{user_hash}\n')
