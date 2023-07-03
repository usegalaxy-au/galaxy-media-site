"""Views for home app."""

import os
import logging
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.loader import get_template
# from pprint import pformat

from utils import aaf
from utils.galaxy import is_registered_galaxy_email
from utils.institution import get_institution_list
from events.models import Event
from news.models import News
from .models import Notice
from .forms import (
    ResourceRequestForm,
    QuotaRequestForm,
    SupportRequestForm,
    AlphafoldRequestForm,
)
from . import subdomains

logger = logging.getLogger('django')


def index(request, landing=False):
    """Show homepage/landing page."""
    news_items = News.objects.filter(is_tool_update=False)
    events = Event.objects.all()
    tool_updates = News.objects.filter(is_tool_update=True)

    if not request.user.is_staff:
        news_items = news_items.filter(is_published=True)
        events = events.filter(is_published=True)
        tool_updates = tool_updates.filter(is_published=True)

    return render(request, 'home/index.html', {
        'landing': landing,
        'notices': Notice.get_notices_by_type(request),
        'news_items': news_items.order_by('-datetime_created')[:6],
        'events': events.order_by('-datetime_created')[:6],
        'tool_updates': tool_updates.order_by('-datetime_created')[:6],
    })


def landing(request, subdomain):
    """Show landing pages for *.usegalaxy.org.au subsites.

    A support request form is passed to the template which can be submitted
    with AJAX and processed by an API handler.
    """
    template = f'home/subdomains/{subdomain}.html'
    try:
        get_template(template)
    except TemplateDoesNotExist:
        raise Http404

    try:
        sections = getattr(subdomains, subdomain).sections
    except AttributeError as exc:
        raise AttributeError(
            f"{exc}\n\n"
            f"No content files found for subdomain '{subdomain}'"
            " at 'webapp/home/subdomains/{subdomain}/'")

    return render(request, template, {
        'name': subdomain,
        'notices': Notice.get_notices_by_type(request, subsite=subdomain),
        'sections': sections,
        'form': SupportRequestForm(),
    })


def notice(request, notice_id):
    """Display notice body page."""
    return render(request, 'home/notice.html', {
        'notice': get_object_or_404(Notice, id=notice_id),
    })


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
            logger.info('Form valid. Dispatch content as email.')
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
        # logger.info(pformat(form.errors))
    return render(request, 'home/requests/tool.html', {'form': form})


def user_request_quota(request):
    """Handle user data quota requests."""
    form = QuotaRequestForm()
    if request.POST:
        form = QuotaRequestForm(request.POST)
        if form.is_valid():
            logger.info('Form valid. Dispatch content as email.')
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
        # logger.info(pformat(form.errors))
    return render(request, 'home/requests/quota.html', {'form': form})


def user_request_support(request):
    """Handle user support requests."""
    form = SupportRequestForm()
    if request.POST:
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
        # logger.info(pformat(form.errors))
    return render(request, 'home/requests/support.html', {'form': form})


def user_request_alphafold(request):
    """Handle alphafold access requests."""
    form = AlphafoldRequestForm()
    if request.POST:
        form = AlphafoldRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if is_registered_galaxy_email(email):
                logger.info(f"Dispatching AlphaFold request for email {email}")
                form.dispatch()
            else:
                logger.info(f"Dispatching AlphaFold warning to {email}")
                form.dispatch_warning(request)
            return render(request, 'home/requests/alphafold-success.html', {
                'email': email,
            })
        logger.info("Form was invalid. Returning invalid feedback.")
        # logger.info(pformat(form.errors))
    return render(request, 'home/requests/alphafold.html', {'form': form})


def page(request):
    """Serve an arbitrary static page."""
    template = f'home/pages/{request.path}'
    templates_dir = os.path.join(
        settings.BASE_DIR,
        'home/templates/home/pages')
    if os.path.basename(template) not in os.listdir(templates_dir):
        raise Http404
    return render(request, template)


def aaf_info(request):
    """Show current list of AAF institutions."""
    return render(request, 'home/aaf-institutions.html', {
        'entities': aaf.get_entities(),
    })


def australian_institutions(request):
    """Show list of recognised AU research institution email domains."""
    return render(request, 'home/au-institutions.html', {
        'institutions': get_institution_list(),
    })
