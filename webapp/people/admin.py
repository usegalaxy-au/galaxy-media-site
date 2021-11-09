"""Register models with the Django admin."""

from django.contrib import admin

from .models import Person
from .forms import PersonAdminForm


class PersonAdmin(admin.ModelAdmin):
    """Administer people."""

    form = PersonAdminForm


admin.site.register(Person, PersonAdmin)
