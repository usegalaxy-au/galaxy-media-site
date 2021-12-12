"""Register models with the Django admin."""

from django.contrib import admin
from django.utils.html import format_html

from .models import Event, EventImage, EventLocation, Tag, Supporter
from .forms import EventAdminForm, TagAdminForm


class EventImageInline(admin.StackedInline):
    """Administer EventImage items."""

    model = EventImage


class EventAdmin(admin.ModelAdmin):
    """Administer event items."""

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

    form = EventAdminForm
    list_display = [
        'id',
        'datetime_created',
        'view_page',
        'title',
        'date_start',
        'date_end',
        'external',
    ]
    inlines = [EventImageInline]

    def render_change_form(self, request, context, *args, **kwargs):
        """Filter objects available in add/change forms."""
        context['adminform'].form.fields['tags'].queryset = (
            Tag.objects.exclude(archived=True))
        context['adminform'].form.fields['supporters'].queryset = (
            Supporter.objects.exclude(archived=True))
        context['adminform'].form.fields['location'].queryset = (
            EventLocation.objects.exclude(archived=True))
        return super(EventAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    @admin.display(empty_value='')
    def view_page(self, obj):
        """Render link to view event page."""
        return format_html("<a href={href}> View page </a>", href=obj.url)

    view_page.short_description = ""
    view_page.allow_tags = True


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
admin.site.register(EventLocation)
