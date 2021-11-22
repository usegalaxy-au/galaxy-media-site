"""Register models with the Django admin."""

from django.contrib import admin
from django.conf import settings

from .models import User, Notice
from .forms import NoticeAdminForm


class NoticeAdmin(admin.ModelAdmin):
    """Administer notices."""

    form = NoticeAdminForm

    class Media:
        """Assets for the admin page."""

        js = (
            '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
            'home/js/admin-mde.js',
        )
        css = {
            'screen': (
                '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
                'home/css/admin-mde.css',
            ),
        }

    list_display = [
        'datetime_modified',
        '__str__',
        'enabled',
    ]


admin.site.site_header = (
    f"Galaxy {settings.GALAXY_SITE_NAME} content administration")
admin.site.register(User)
admin.site.register(Notice, NoticeAdmin)
