"""Register models with the Django admin."""

from django.contrib import admin

from .models import Event, Tag, Supporter
from .forms import EventAdminForm


class EventAdmin(admin.ModelAdmin):
    """Administer event items."""

    form = EventAdminForm


admin.site.register(Event, EventAdmin)
admin.site.register(Tag)
admin.site.register(Supporter)
