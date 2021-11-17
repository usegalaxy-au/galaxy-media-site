"""Signals define various hooks which perform a function on a given event.

Events include pre_save, post_save, pre_delete, post_delete.

Typical usage might be deleting files associated with a model instance using a
post_delete hook or modifying the model instance attributes before saving with
a pre_save hook.

Signals may be fired in duplicate in testing, so it is best to guard them
against double-firing (e.g. check if file exists before creating).

Must be called in apps.py to work.
"""

from django.dispatch import receiver
from django.db.models.signals import (
    # pre_delete,
    # post_delete,
    # pre_save,
    post_save,
)

from .models import Event, EventImage


@receiver(post_save, sender=Event)
def render_markdown_image_uris(sender, instance, using, **kwargs):
    """Replace EventImage identifiers with real URIs in submitted markdown.

    !!! Need to validate markdown on submission.

    !!! Probably needs to be called from EventImage.post_save
    """
    body = instance.body
    images = (
        EventImage.objects.filter(event_id=instance.id)
        .order_by('id')
    )
    for i, image in enumerate(images):
        body = body.replace(
            f"(img{i + 1})",
            f"({image.img_uri})")
    Event.objects.filter(id=instance.id).update(body=body)
