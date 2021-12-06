"""Event views."""

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Event


def index(request):
    """Show events list page."""
    if request.user.is_staff:
        events = Event.objects.all()
    else:
        events = Event.objects.filter(is_published=True)
    return render(request, 'events/index.html', {
        'events': events.order_by('-date_start'),
    })


def show(request, pk=None):
    """Show event article page."""
    if not pk:
        raise Http404
    try:
        return render(request, 'events/event.html', {
            'event': Event.objects.get(id=pk),
        })
    except ObjectDoesNotExist:
        raise Http404


def ical(request, pk=None):
    """Return a calendar event in iCal format.

    Can validate by copying event.ics browser source into
    https://icalendar.org/validator.html.
    """
    if not pk:
        raise Http404
    try:
        return render(request, 'events/event.ics', {
            'event': Event.objects.get(id=pk),
        })
    except ObjectDoesNotExist:
        raise Http404
