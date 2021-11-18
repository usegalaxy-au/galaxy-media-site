"""Register models with the Django admin."""

from django.contrib import admin

from .models import News, NewsImage
from .forms import NewsAdminForm


class NewsImageInline(admin.StackedInline):
    """Administer NewsImage items."""

    model = NewsImage


class NewsAdmin(admin.ModelAdmin):
    """Administer news items."""

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

    form = NewsAdminForm
    list_display = [
        'datetime_created',
        'title',
        'external',
    ]
    inlines = [NewsImageInline]


admin.site.register(News, NewsAdmin)
