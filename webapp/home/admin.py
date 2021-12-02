"""Register models with the Django admin."""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings

from .models import User, Notice
from .forms import NoticeAdminForm, UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    """Administer users."""

    form = UserChangeForm
    add_form = UserCreationForm

    # Remove username field
    ordering = [
        'first_name',
        'last_name',
        'email',
        'password',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_display = [
        'first_name',
        'last_name',
        'email',
    ]
    list_filter = ['is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'user_permissions',
        )}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


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
admin.site.register(User, UserAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.unregister(Group)
