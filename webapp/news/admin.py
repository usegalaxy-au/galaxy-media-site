"""Register models with the Django admin."""

from django.contrib import admin
from django.utils.html import format_html

from events.models import Tag, Supporter
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
            'home/js/admin-required-fields.js',
            'home/js/admin-mde.js',
        )
        css = {
            'screen': (
                '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
                'home/css/admin-mde.css',
            ),
        }

    def render_change_form(self, request, context, *args, **kwargs):
        """Filter objects available in add/change forms."""
        context['adminform'].form.fields['tags'].queryset = (
            Tag.objects.exclude(archived=True))
        context['adminform'].form.fields['supporters'].queryset = (
            Supporter.objects.exclude(archived=True))
        return super(NewsAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    form = NewsAdminForm
    list_display = [
        'id',
        'view_page',
        'datetime_created',
        'title',
        'external',
    ]
    inlines = [NewsImageInline]
    order = ('-datetime_created',)

    @admin.display(empty_value='')
    def view_page(self, obj):
        """Render link to view news article page."""
        return format_html("<a href={href}> View page </a>", href=obj.url)


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
