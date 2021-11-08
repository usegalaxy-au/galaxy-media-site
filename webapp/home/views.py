"""Views for home app."""

from datetime import datetime
from django.shortcuts import render

FAKE_NEWS_ITEMS = [
    {
        'date': datetime.strptime('2021-10-28', '%Y-%m-%d'),
        'icons': ['build'],
        'title': "Galaxy australia tool updates",
    },
    {
        'date': datetime.strptime('2021-10-10', '%Y-%m-%d'),
        'icons': [],
        'title': "Intergalactic news",
    },
    {
        'date': datetime.strptime('2021-10-04', '%Y-%m-%d'),
        'icons': ['build'],
        'title': "Galaxy australia tool updates",
    },
    {
        'date': datetime.strptime('2021-10-28', '%Y-%m-%d'),
        'icons': ['build'],
        'title': "Galaxy australia tool updates",
    },
    {
        'date': datetime.strptime('2021-10-10', '%Y-%m-%d'),
        'icons': [],
        'title': "Intergalactic news",
    },
    {
        'date': datetime.strptime('2021-10-04', '%Y-%m-%d'),
        'icons': ['build'],
        'title': "Galaxy australia tool updates",
    },
]

FAKE_EVENT_ITEMS = [
    {
        'date': datetime.strptime('2021-10-07', '%Y-%m-%d'),
        'icons': ['school', 'event'],
        'title': "WORKSHOP: Hybrid de novo genome assembly",
    },
    {
        'date': datetime.strptime('2021-09-16', '%Y-%m-%d'),
        'icons': ['event'],
        'title': "Galaxy Paper Cuts",
    },
    {
        'date': datetime.strptime('2021-09-09', '%Y-%m-%d'),
        'icons': ['school', 'event'],
        'title': "WORKSHOP: Online data analsis for biologists",
    },
    {
        'date': datetime.strptime('2021-06-28', '%Y-%m-%d'),
        'icons': ['groups', 'event'],
        'title': "Galaxy community conference (GCC 2021) - virtual edition",
    },
]

# Should upgrade to class-based views


def index(request):
    """Return homepage."""
    return render(request, 'home/index.html', {
        'news_items': FAKE_NEWS_ITEMS,
        'event_items': FAKE_EVENT_ITEMS,
    })
