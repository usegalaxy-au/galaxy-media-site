"""People views."""

from django.shortcuts import render

from .models import Person


def index(request):
    """Show people page."""
    return render(request, 'people/index.html', {
        'people': Person.objects.order_by('ranking', 'datetime_created'),
    })
