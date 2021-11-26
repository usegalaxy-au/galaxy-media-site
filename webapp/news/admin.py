"""Register models with the Django admin."""

from django.contrib import admin

from .models import News, NewsImage, APIToken
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


class APITokenAdmin(admin.ModelAdmin):
    """Administer API tokens."""

    def render_change_form(self, request, context, *args, **kwargs):
        """Define a custom template."""
        self.change_form_template = 'news/admin/apitoken-form.html'
        extra = {
            'help_text': (
                'These API tokens grant API access for automated posting of'
                ' News items. <br>'
                '<b>Treat them as secrets</b>'
                ' - anyone with an API token can create posts on the site!<br>'
                'The token will become visible after saving.'
            ),
        }
        context.update(extra)
        return super().render_change_form(request, context, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """Return read-only fields to display."""
        if obj:
            # Object exists, show token field
            return self.readonly_fields
        return ()

    readonly_fields = ['token']


admin.site.register(News, NewsAdmin)
admin.site.register(APIToken, APITokenAdmin)
