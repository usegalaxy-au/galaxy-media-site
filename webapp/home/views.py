"""Views for home app."""

import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseNotFound

from home.models import Notice
from events.models import Event
from news.models import News


def index(request, landing=False):
    """Show homepage/landing page."""
    if request.user.is_staff:
        news_items = News.objects.all()
        events = Event.objects.all()
        notices = Notice.objects.filter(enabled=True)
    else:
        news_items = News.objects.filter(is_published=True)
        events = Event.objects.filter(is_published=True)
        notices = Notice.objects.filter(enabled=True, is_published=True)

    return render(request, 'home/index.html', {
        'news_items': news_items.order_by('-datetime_created')[:6],
        'events': events.order_by('-datetime_created')[:6],
        'notices': notices.order_by('order'),
        'landing': landing,
    })


def landing(request):
    """Show landing page for usegalaxy.org.au.

    Same as index but without the navbar.
    """
    return index(request, landing=True)


def about(request):
    """Show about page."""
    return render(request, 'home/about.html')


def support(request):
    """Show support page."""
    return render(request, 'home/support.html')


def page(request):
    """Serve an arbitrary static page."""
    template = f'home/pages/{request.path}'
    templates_dir = os.path.join(
        settings.BASE_DIR,
        'home/templates/home/pages')
    if os.path.basename(template) not in os.listdir(templates_dir):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template)
