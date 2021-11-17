"""Signals define various hooks which perform a function on a given event.

Events include pre_save, post_save, pre_delete, post_delete.

Typical usage might be deleting files associated with a model instance using a
post_delete hook or modifying the model instance attributes before saving with
a pre_save hook.

Signals may be fired in duplicate in testing, so it is best to guard them
against double-firing (e.g. check if file exists before creating).

Must be called in apps.py to work.
"""

import re
from django.dispatch import receiver
from django.db.models.signals import (
    # pre_delete,
    # post_delete,
    # pre_save,
    post_save,
)

from .models import Event, EventImage


@receiver(post_save, sender=EventImage)
def render_markdown_image_uris(sender, instance, using, **kwargs):
    """Replace EventImage identifiers with real URIs in submitted markdown.

    !!! Need to validate markdown on submission.

    !!! Probably needs to be called from EventImage.post_save
    """
    event = Event.objects.get(id=instance.event_id)
    p = re.compile(r'\(img\d\)', re.MULTILINE)
    m = p.search(event.body)
    if not m:
        # No tags to replace
        return

    # Determine current event image number
    i = 1
    while f"(img{i})" not in event.body:
        i += 1

    # Replace placeholder with real URI
    event.body = event.body.replace(
        f"(img{i})",
        f"({instance.img_uri})")
    event.save()
