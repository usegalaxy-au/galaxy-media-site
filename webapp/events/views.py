"""Event views."""

from django.shortcuts import render

from .models import Event


def index(request):
    """Show events list page."""
    return render(request, 'events/index.html', {
        'events': Event.objects.order_by('datetime_created'),
    })
