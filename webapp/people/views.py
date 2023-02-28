"""People views."""

from django.shortcuts import render

from .models import Person


def index(request):
    """Show people page."""
    people = Person.objects.order_by('ranking', 'datetime_created')
    return render(request, 'people/index.html', {
        'people': people.filter(alumni=False),
        'alumni': people.filter(alumni=True),
    })
