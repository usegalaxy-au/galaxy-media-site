"""Views for home app."""

from django.shortcuts import render

from events.models import Event
from news.models import News

# Should upgrade to class-based views


def index(request):
    """Return homepage."""
    return render(request, 'home/index.html', {
        'news_items': News.objects.order_by('-datetime_created')[:6],
        'events': Event.objects.order_by('-datetime_created')[:6],
    })
