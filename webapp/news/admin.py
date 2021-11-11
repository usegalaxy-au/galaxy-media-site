"""Register models with the Django admin."""

from django.contrib import admin

from .models import News
from .forms import NewsAdminForm


class NewsAdmin(admin.ModelAdmin):
    """Administer news items."""

    form = NewsAdminForm
    list_display = [
        'datetime_created',
        'title',
        'external',
    ]


admin.site.register(News, NewsAdmin)
