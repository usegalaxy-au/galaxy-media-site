"""Parser functions for extracting fields from text."""

import os
import json
import datetime


def organiser_name(meta):
    """Get name from organiser text."""
    v = meta.get('organiser') or ''
    assert type(v) in (dict, str), f"{type(v)} found"
    if type(v) == dict:
        return v.get('name', '')
    return v


def organiser_email(meta):
    """Get email from organiser text."""
    v = meta.get('organiser') or ''
    if type(v) == dict:
        return v.get('email', '')
    return ''


def location_json(meta):
    """Get location data from location text."""
    v = meta.get('location')
    if not v:
        return ''
    if type(v) == str:
        v = {'name': v.title()}
    return json.dumps(v)


def date_start(meta):
    """Get start date."""
    v = meta.get('starts') or ''
    assert type(v) == datetime.date or type(v) == str, (
        f"{type(v)} found")
    if type(v) == datetime.date:
        return v.strftime('%Y-%m-%d')
    return v


def date_end(meta):
    """Get end date."""
    v = meta.get('ends') or ''
    assert type(v) == datetime.date or type(v) == str, (
        f"{type(v)} found")
    if type(v) == datetime.date:
        return v.strftime('%Y-%m-%d')
    return v


def date_from_filepath(path):
    """Parse date from filename."""
    fname = os.path.basename(path)
    date = fname[:10]
    # Assert dt format
    datetime.datetime.strptime(date, '%Y-%m-%d')
    return date


def csv_escape(text):
    """Escape functional characters in text for embedding in CSV."""
    if text is None:
        return ''
    return '~' + text.strip('\n -') + '~'
