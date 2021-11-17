"""Register models with the Django admin."""

from django.contrib import admin

from .models import Event, EventImage, Tag, Supporter
from .forms import EventAdminForm, TagAdminForm


class EventImageInline(admin.StackedInline):
    """Administer EventImage items."""

    model = EventImage


class EventAdmin(admin.ModelAdmin):
    """Administer event items."""

    form = EventAdminForm
    list_display = [
        'datetime_created',
        'title',
        'external',
        'organiser_name',
        'organiser_email',
        'timezone',
        'date_start',
        'date_end',
    ]
    inlines = [EventImageInline]


class TagAdmin(admin.ModelAdmin):
    """Administer tag items."""

    form = TagAdminForm
    list_display = [
        'name',
        'color',
        'archived',
    ]


class SupporterAdmin(admin.ModelAdmin):
    """Administer supporter items."""

    list_display = [
        'name',
        'url',
        'logo_img',
        'archived',
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Supporter)
