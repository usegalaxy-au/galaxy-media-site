"""Event views."""

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Event


def index(request):
    """Show events list page."""
    return render(request, 'events/index.html', {
        'events': Event.objects.order_by('-date_start'),
    })


def show(request, pk=None):
    """Show event article page."""
    if not pk:
        return
    try:
        return render(request, 'events/event.html', {
            'event': Event.objects.get(id=pk),
        })
    except ObjectDoesNotExist:
        raise Http404
