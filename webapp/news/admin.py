"""Register models with the Django admin."""

from django.contrib import admin

from .models import News, NewsImage
from .forms import NewsAdminForm


class NewsImageInline(admin.StackedInline):
    """Administer NewsImage items."""

    model = NewsImage


class NewsAdmin(admin.ModelAdmin):
    """Administer news items."""

    form = NewsAdminForm
    list_display = [
        'datetime_created',
        'title',
        'external',
    ]
    inlines = [NewsImageInline]


admin.site.register(News, NewsAdmin)
