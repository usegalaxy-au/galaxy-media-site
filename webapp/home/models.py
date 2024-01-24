"""Models for storing generic and homepage content."""

import os
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from random import shuffle
from urllib.parse import urljoin

from .managers import CustomUserManager
from . import help_text


def get_upload_path(instance, filename):
    """Return media path for uploaded images."""
    return f"uploads/images/{filename}"


def default_subsite():
    """The first ID will always be 'main', as created in migration."""
    return [1]


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
    """Galaxy subsite which will consume a custom landing page.

    The migration for this model creates a default 'main' subsite.
    """

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

    All notices will shown as rotating - displayed in a top banner and cycled
    through by fade in/out such that multiple notices can be displayed without
    clogging up the UI.

    Notices can be also be displayed as static by setting
    ``static_display = True``.
    """

    NOTICE_CLASSES = (
        ('info', 'info'),
        ('warning', 'warning'),
        ('none', 'image'),
    )

    datetime_modified = models.DateTimeField(auto_now=True)
    notice_class = models.CharField(
        max_length=16, choices=NOTICE_CLASSES, default='',
        help_text=help_text.Notice.NOTICE_CLASS,
    )
    static_display = models.BooleanField(
        default=False,
        help_text=help_text.Notice.STATIC_DISPLAY,
    )
    title = models.CharField(max_length=100, blank=True)
    display_title = models.BooleanField(
        default=True,
        help_text=(
            "Show the notice title when displaying as a static"
            " notice. This option is ignored for image notices.")
    )
    short_description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text=help_text.Notice.SHORT_DESCRIPTION,
    )
    body = models.CharField(
        max_length=10000,
        null=True,
        blank=True,
        help_text=help_text.Notice.BODY,
    )
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=help_text.Notice.MATERIAL_ICON,
    )
    enabled = models.BooleanField(
        default=False,
        help_text="Display on the Galaxy Australia landing page."
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Unpublished content is visible to admin users only."
            " Use this to review content before release to public users."
        ),
    )
    order = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text=(
            "Display order on the landing page when multiple <em>static</em>"
            " notices are enabled (i.e. lowest value shown first)"
        ),
    )
    subsites = models.ManyToManyField(
        Subsite,
        help_text=(
            "Select which subdomain sites should display the notice."
        ),
        default=default_subsite,
    )

    @classmethod
    def get_notices_by_type(cls, request, subsite=None):
        """Return dictionary of notices by type for given user."""
        subsite_name = subsite or 'main'
        notices = cls.objects.filter(
            enabled=True,
            subsites__name=subsite_name,
        )
        if not request.user.is_staff:
            notices = notices.filter(is_published=True)

        # Separate notices for static/rotating display
        text_notices = notices.exclude(notice_class='none')
        dismissed = request.session.get('dismissed_notices', [])
        static_notices = [
            n for n in
            text_notices.filter(static_display=True).order_by('order')
            if n.timestamp not in dismissed
        ]
        rotating_notices = list(text_notices.exclude(static_display=True))
        shuffle(rotating_notices)
        all_rotating_notices = (
            list(text_notices.exclude(static_display=False))
            + rotating_notices
        )
        return {
            'image': None,  # image_notices are deprecated
            'rotating': all_rotating_notices,
            'static': static_notices,
        }

    @property
    def timestamp(self):
        """Return timestamp for notice."""
        return self.datetime_modified.isoformat()

    @property
    def url(self):
        """Return the URL for this notice."""
        return f"/notice/{self.id}"

    def __str__(self):
        """Return string representation."""
        return f"[{self.get_notice_class_display()}] {self.title}"

    def clean(self):
        """Clean fields before saving."""
        super().clean()
        if self.material_icon:
            self.material_icon = self.material_icon.lower().replace(' ', '_')


class CoverImage(models.Model):
    """A banner-style image on the landing page."""

    datetime_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, help_text=(
        "This will be used to identify the image in the web admin, and for"
        " accessibility purposes (i.e. screen-readers) on the webpage."
    ))
    img = models.FileField(
        upload_to=get_upload_path,
        help_text=help_text.CoverImage.IMG)
    max_height_px = models.IntegerField(
        default=300,
        verbose_name="Max height (px)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ],
        help_text=help_text.CoverImage.DISPLAY_HEIGHT)
    auto_full_width = models.BooleanField(default=False, help_text=(
        "Automatically set the image width to 100% of the screen width."
        " This option overrides 'Max height'."
    ))
    enabled = models.BooleanField(
        default=False,
        help_text="Display on the Galaxy Australia landing page."
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
        default=default_subsite,
    )

    @classmethod
    def get_random(cls, request, subsite=None):
        """Return a random cover image."""
        subsite_name = subsite or 'main'
        images = cls.objects.filter(
            enabled=True,
            subsites__name=subsite_name,
        )
        if not request.user.is_staff:
            images = images.filter(is_published=True)
        return images.order_by('?').first()


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
