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

from .models import News, NewsImage
from utils.markdown import render_image_uri


@receiver(post_save, sender=NewsImage)
def render_markdown_image_uris(sender, instance, using, **kwargs):
    """Replace NewsImage identifiers with real URIs in submitted markdown.

    !!! Need to validate markdown on submission.
    """
    article = News.objects.get(id=instance.news_id)
    render_image_uri(article, instance.img_uri)
