"""Views for home app."""

import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from pprint import pprint

from events.models import Event
from news.models import News
from .models import Notice
from .forms import ResourceRequestForm, QuotaRequestForm, SupportRequestForm


def index(request, landing=False):
    """Show homepage/landing page."""
    if request.user.is_staff:
        news_items = News.objects.all()
        events = Event.objects.all()
    else:
        news_items = News.objects.filter(is_published=True)
        events = Event.objects.filter(is_published=True)

    return render(request, 'home/index.html', {
        'news_items': news_items.order_by('-datetime_created')[:6],
        'events': events.order_by('-datetime_created')[:6],
        'notices': Notice.objects.filter(enabled=True).order_by('order'),
        'landing': landing,
    })


def landing(request):
    """Show landing page for usegalaxy.org.au."""
    return index(request, landing=True)


def about(request):
    """Show about page."""
    return render(request, 'home/about.html')


def user_request(request):
    """Show user request menu."""
    return render(request, 'home/requests/menu.html')


def user_request_tool(request):
    """Handle user tool requests."""
    form = ResourceRequestForm()
    if request.POST:
        form = ResourceRequestForm(request.POST)
        if form.is_valid():
            template = (
                'home/requests/mail/'
                f"{form.cleaned_data['resource_type']}.html"
            )
            html_message = render_to_string(template, {'form': form})
            form.dispatch(html_message)
            return user_request_success(request)
        print("Form was invalid")
        pprint(form.errors)
    return render(request, 'home/requests/tool.html', {'form': form})


def user_request_quota(request):
    """Handle user data quota requests."""
    form = QuotaRequestForm()
    if request.POST:
        form = QuotaRequestForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return user_request_success(request)
        print("Form was invalid")
        pprint(form.errors)
    return render(request, 'home/requests/quota.html', {'form': form})


def user_request_support(request):
    """Handle user support requests."""
    form = SupportRequestForm()
    if request.POST:
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return user_request_success(request)
        print("Form was invalid")
        pprint(form.errors)
    return render(request, 'home/requests/support.html', {'form': form})


def user_request_success(request):
    """Show success page after form submission."""
    return render(request, 'home/requests/success.html')


def page(request):
    """Serve an arbitrary static page."""
    template = f'home/pages/{request.path}'
    templates_dir = os.path.join(
        settings.BASE_DIR,
        'home/templates/home/pages')
    if os.path.basename(template) not in os.listdir(templates_dir):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template)
