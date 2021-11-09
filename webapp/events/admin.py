"""Register models with the Django admin."""

from django.contrib import admin

from .models import Event, Tag, Supporter
from .forms import EventAdminForm, TagAdminForm


class EventAdmin(admin.ModelAdmin):
    """Administer event items."""

    form = EventAdminForm


class TagAdmin(admin.ModelAdmin):
    """Administer tag items."""

    form = TagAdminForm


admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Supporter)
