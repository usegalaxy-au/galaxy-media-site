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
        ('none', 'image'),
    )

    datetime_modified = models.DateTimeField(auto_now=True)
    notice_class = models.CharField(
        max_length=16, choices=NOTICE_CLASSES, default='',
        help_text=(
"""
<ul style='margin-left: 2rem;'>
    <li style='list-style: disc;'>
        A style class to set a color scheme for the notice - uses
        <a
            href='https://getbootstrap.com/docs/5.0/components/alerts/'
            target='_blank'
        >standard bootstrap styling</a>
        (
            <em>info</em>: blue,
            <em>warning</em>: orange,
            <em>danger</em>: red
        ).
    </li>
    <li style='list-style: disc;'>
        Use the <em>image</em> class for displaying an image. For this,
        the body should consist of an HTML <code>&lt;img&gt;</code> tag
        only (or markdown equivalent).
    </li>
    <li style='list-style: disc;'>
        Static notices show the <b>body</b> on the landing page instead
        of the <b>short description</b> and do not link to a webpage.
    </li>
    <li style='list-style: disc;'>
        An image notice will always be displayed as a static block, with
        no title/description text. Use for displaying banners e.g.
        event posters.
    </li>
</ul>
"""
        )
    )
    static_display = models.BooleanField(
        default=False,
        help_text=(
"""
<ul style='margin-left: 2rem;'>
    <li style='list-style: disc;'>
        Display the notice as a static block beneath the GA logo, rather than
        the default rotating notice (i.e. the banner beneath the navbar).
    </li>
    <li style='list-style: disc;'>
        Ideally, this should only be checked for
        <b style='color: firebrick;'>a single, high-priority notice</b>
        to prevent cluttering of the landing page.
    </li>
    <li style='list-style: disc;'>
        Static notices show the <b>body</b> on the landing page instead
        of the <b>short description</b> and do not link to a webpage.
    </li>
    <li style='list-style: disc;'>
        Notices with <em>image</em> class always have static display,
        so this option will be ignored.
    </li>
</ul>
"""
        )
    )
    title = models.CharField(max_length=100)
    display_title = models.BooleanField(
        default=True,
        help_text=(
            "Show the notice title when displaying as a static"
            " notice. The title is always shown on the notice webpage"
            " for non-static (rotating) notices.")
    )
    short_description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=(
"""
<ul style='margin-left: 2rem;'>
    <li style='list-style: disc;'>
        This will be displayed on the landing page (200 char max) as plain
        text or inline HTML (e.g.
        <code>&lt;a&gt;</code>,
        <code>&lt;b&gt;</code>
        tags).
    </li>
    <li style='list-style: disc;'>
        If not <em>static</em> display (default), this will be shown as a
        single line of text above the navbar,
        <b>which will be cut off if too long</b>,
        especially on small screens!
    </li>
    <li style='list-style: disc;'>
        If <em>static</em> display is enabled, this field is ignored in favour
        of the <em>title</em> and <em>body</em> fields.
    </li>
</ul>
"""
        ),
    )
    body = models.CharField(max_length=10000, null=True, blank=True,
        help_text=(
            MARKDOWN_HELP_TEXT + "<br><br>"
            "Unless <em>static display</em> is enabled,"
            " <b>This text will be displayed on a dedicated webpage</b>"
            " that is linked to from the landing page notice."
            " If this field is left blank, there will be no link."
            )
    )
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=('Optional. A valid Material Design icon ID to be'
                   ' displayed with the title (e.g. <em>check_box</em>).'
                   ' <a href="https://fonts.google.com/icons" target="_blank">'
                   ' Browse 2500+ icons here </a>.')
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
