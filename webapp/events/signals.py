"""Signals define various hooks which perform a function on a given event.

Events include pre_save, post_save, pre_delete, post_delete.

Typical usage might be deleting files associated with a model instance using a
post_delete hook or modifying the model instance attributes before saving with
a pre_save hook.

Signals may be fired in duplicate in testing, so it is best to guard them
against double-firing (e.g. check if file exists before creating).

Must be called in apps.py to work.
"""

import os
from django.dispatch import receiver
from django.db.models.signals import (
    # pre_delete,
    post_delete,
    pre_save,
    post_save,
)

from .models import Event, EventImage


@receiver(post_save, sender=EventImage)
def render_markdown_image_uris(sender, instance, using, **kwargs):
    """Replace EventImage identifiers with real URIs in submitted markdown."""
    event = Event.objects.get(id=instance.event_id)
    event.render_markdown_uris()


@receiver(post_delete, sender=EventImage)
def delete_image_file(sender, instance, using, **kwargs):
    """Delete image file if it exists."""
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(pre_save, sender=EventImage)
def delete_old_image_file(sender, instance, using, **kwargs):
    """Delete old image file if it exists."""
    if not instance.id:
        return False

    try:
        old_image = EventImage.objects.filter(id=instance.id)
    except EventImage.DoesNotExist:
        return False

    if (
        old_image.file != instance.file
        and os.path.isfile(old_image.file)
    ):
        old_image.file.delete(save=False)
