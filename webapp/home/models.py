"""Models for storing generic and homepage content."""

from django.db import models
from django.contrib.auth.models import AbstractUser

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


class Notice(models.Model):
    """A site notice to be displayed on the home/landing pages."""

    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'

    NOTICE_CLASSES = (
        (INFO, 'info'),
        (WARNING, 'warning'),
        (DANGER, 'danger'),
    )

    datetime_modified = models.DateTimeField(auto_now=True)
    notice_class = models.CharField(
        max_length=16, choices=NOTICE_CLASSES, default=INFO,
    )
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=2000, help_text='Enter valid markdown')
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=('Optional. A valid Material Design icon identifier.'
                   ' <a href="https://fonts.google.com/icons" target="_blank">'
                   ' Browse icons here </a>')
        )
    enabled = models.BooleanField(
        default=False,
        help_text="Display on the Galaxy Australia landing page.")

    def __str__(self):
        """Return string representation."""
        return f"[{self.notice_class}] {self.title}"

    def clean(self):
        """Clean fields before saving."""
        super().clean()
        if self.material_icon:
            self.material_icon = self.material_icon.lower().replace(' ', '_')
