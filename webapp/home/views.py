"""Views for home app."""

import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseNotFound

from events.models import Event
from news.models import News

# Should maybe upgrade to class-based views?


def index(request):
    """Show homepage."""
    return render(request, 'home/index.html', {
        'news_items': News.objects.order_by('-datetime_created')[:6],
        'events': Event.objects.order_by('-datetime_created')[:6],
    })


def landing(request):
    """Show landing page for usegalaxy site."""
    return render(request, 'home/index.html', {
        'landing': True,
        'news_items': News.objects.order_by('-datetime_created')[:6],
        'events': Event.objects.order_by('-datetime_created')[:6],
    })


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
