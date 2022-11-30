"""Models for storing generic and homepage content."""

import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from urllib.parse import urljoin

from utils.markdown import MARKDOWN_HELP_TEXT
from .managers import CustomUserManager


class User(AbstractUser):
    """Staff user for managing site content."""

    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        """Return a string representation of self."""
        return f"{self.first_name} {self.last_name} <{self.email}>"


class Subsite(models.Model):
    """Galaxy subsite which will consume a custom landing page."""

    name = models.CharField(max_length=30, unique=True, help_text=(
        "This field should match the subdomain name. e.g."
        " for a 'genome.usegalaxy.org' subsite, the name should be 'genome'."
        " This also determines the URL as: '/landing/<subsite.name>'. The"
        " HTML template for this landing page must be created manually."
    ))

    def __str__(self):
        """Represent self as string."""
        return self.name


class Notice(models.Model):
    """A site notice to be displayed on the home/landing pages.

    A notice contains a brief message for display on the home page, and a
    longer message that will be linked to on a separate page.

    Notices of lower priority will be cycled through by fade in/out such
    that multiple notices can be displayed without clogging up the UI.

    Notices of the 'danger' class will always be displayed, in addition to
    the others.
    """

    NOTICE_CLASSES = (
        ('info', 'info'),
        ('warning', 'warning'),
        ('danger', 'danger'),
        ('none', 'none'),
    )

    datetime_modified = models.DateTimeField(auto_now=True)
    notice_class = models.CharField(
        max_length=16, choices=NOTICE_CLASSES, default='',
        help_text=(
            "A style class to set a color scheme for the notice. Select"
            " <em>none</em> for no styling (e.g. inserting an image).<br>"
            " <b>Notices with the <em>danger</em> class will always be"
            " displayed.</b> All other notices will be cycled through when"
            " multiple notices are enabled."
        )
    )
    title = models.CharField(max_length=100)
    display_title = models.BooleanField(
        default=True,
        help_text="Uncheck to hide the title when displaying the notice.")
    short_description = models.CharField(
        max_length=200,
        help_text=(
            "This will be displayed on the landing page (max 200 chars)."
            " Plain text or inline HTML e.g. &lt;b&gt;, &lt;img&gt;."
            " Will be displayed with a max height of 100px."))
    body = models.CharField(max_length=10000, null=True, blank=True,
        help_text=(
            "<b>This text will be displayed on a dedicated webpage</b>"
            " - if this field is blank, no link will be displayed.<br><br>"
            + MARKDOWN_HELP_TEXT)
    )
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=('Optional. A valid Material Design icon identifier to be'
                   ' displayed with the title.'
                   ' <a href="https://fonts.google.com/icons" target="_blank">'
                   ' Browse icons here </a>')
    )
    enabled = models.BooleanField(
        default=False,
        help_text="Display on the Galaxy Australia landing page.")
    order = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text=("Order of display on the landing page when multiple Notices"
                   " are enabled (i.e. lowest value shown first)")
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Unpublished content is visible to admin users only."
            " Use this to review content before release to public users."
        ),
    )
    subsites = models.ManyToManyField(
        Subsite,
        help_text=(
            "Select which subdomain sites should display the notice."
        ),
    )

    def __str__(self):
        """Return string representation."""
        return f"[{self.get_notice_class_display()}] {self.title}"

    @property
    def url(self):
        """Return the URL for this notice."""
        return f"/notice/{self.id}"

    def clean(self):
        """Clean fields before saving."""
        super().clean()
        if self.material_icon:
            self.material_icon = self.material_icon.lower().replace(' ', '_')


def get_upload_path(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/images/{filename}"


class MediaImage(models.Model):
    """An uploaded images that can be served as a media file."""

    image = models.FileField(
        upload_to=get_upload_path,
    )

    @property
    def uri(self):
        """Return media URI for image."""
        return urljoin(settings.MEDIA_URL, str(self.image))

    @property
    def filename(self):
        """Return string filename."""
        return os.path.basename(str(self.image))
