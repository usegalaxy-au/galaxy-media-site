"""Functions for unsubscribing user from mail."""

import pandas as pd
from django.conf import settings


def add(user_hash):
    """Add user email to unsubscribe list."""
    records = pd.read_csv(settings.RECIPIENT_MASTER_CSV)
    records.loc[records['hash'] == user_hash, 'excluded_by'] = 'GMS'
    records.to_csv(settings.RECIPIENT_MASTER_CSV)
