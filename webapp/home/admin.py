"""Register models with the Django admin."""

from django.contrib import admin

from .models import User, Notice
from .forms import NoticeAdminForm


class NoticeAdmin(admin.ModelAdmin):
    """Administer notices."""

    form = NoticeAdminForm


admin.site.site_header = "Galaxy Australia content administration"
admin.site.register(User)
admin.site.register(Notice, NoticeAdmin)
