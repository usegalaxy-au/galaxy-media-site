"""Views for home app."""

import os
import logging
import pprint
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader, TemplateDoesNotExist

from events.models import Event
from news.models import News
from utils import aaf
from utils import unsubscribe
from utils.exceptions import ResourceAccessError
from .models import CoverImage, Notice
from .forms import (
    ResourceRequestForm,
    QuotaRequestForm,
    SupportRequestForm,
    ACCESS_FORMS,
)
from . import pages_context

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
        'cover_image': CoverImage.get_random(request),
        'news_items': news_items.order_by('-datetime_created')[:6],
        'events': events.order_by('-datetime_created')[:6],
        'tool_updates': tool_updates.order_by('-datetime_created')[:6],
    })


def landing(request, subdomain):
    """Show landing pages for *.usegalaxy.org.au subsites.

    DEPRECATED: This view is deprecated in favour of labs.usegalaxy.org.au.
    """
    return render(request, 'home/labs-deprecated.html')


def export_lab(request):
    """Generic Galaxy Lab landing page build with externally hosted content.

    DEPRECATED: This view is deprecated in favour of labs.usegalaxy.org.au.
    """
    return render(request, 'home/labs-deprecated.html')


def notice(request, notice_id):
    """Display notice body page."""
    return render(request, 'home/notice.html', {
        'notice': get_object_or_404(Notice, id=notice_id),
    })


def about(request):
    """Show about page."""
    return render(request, 'home/about.html')


def acknowledge(request):
    """Show acknowledge page."""
    return render(request, 'home/acknowledge.html')


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
    return render(request, 'home/requests/support.html', {'form': form})


def user_request_resource_index(request):
    """Handle user support requests."""
    return render(request, 'home/requests/access/index.html')


def user_request_resource_access(request, resource):
    """Handle resource (e.g. tool) access requests.

    The galaxy group name must match the <resource> string encoded in the URL.
    """
    if resource not in ACCESS_FORMS:
        raise Http404
    Form = ACCESS_FORMS[resource]
    form = Form()
    if request.POST:
        form = Form(request.POST)
        if form.is_valid():
            try:
                actioned = form.action(request, resource)
            except ResourceAccessError as exc:
                logger.error(
                    f"ResourceAccessError for {resource}:\n{exc}"
                    f"Form data:\n{pprint.pformat(form.cleaned_data)}")
                return report_exception_response(
                    request,
                    exc,
                    title=("Sorry, an error occurred while actioning your"
                           " request"),
                )
            success_template = 'home/requests/access/success.html'
            return render(request, success_template, {
                'form': form.cleaned_data,
                'actioned': actioned,
            })
        logger.info("Form was invalid. Returning invalid feedback.")
    template = f'home/requests/access/{resource}.html'
    return render(request, template, {'form': form})


def report_exception_response(request, exc, title=None):
    """Report an exception to the user."""
    return render(request, 'generic.html', {
        'message': str(exc),
        'title': title or "Sorry, an error has occurred",
    })


def page(request):
    """Serve an arbitrary static page."""
    # Get template
    path = request.path.strip('/')
    template = f'home/pages/{path}'
    templates_dir = os.path.join(
        settings.BASE_DIR,
        'home/templates/home/pages')
    if os.path.basename(template) not in os.listdir(templates_dir):
        raise Http404

    if path.endswith('.md'):
        return md_page(request, template)

    # Get context
    context = pages_context.get(path)
    return render(request, template, context)


def md_page(request, template):
    """Return a markdown file rendered to HTML."""
    md_path = (
        loader.get_template(template)
        .origin.name
    )
    with open(md_path) as f:
        markdown = f.read()
    return render(request, 'home/markdown-page.html', {
        'md_text': markdown,
    })


def aaf_info(request):
    """Show current list of AAF institutions."""
    return render(request, 'home/aaf-institutions.html', {
        'entities': aaf.get_entities(),
    })


def unsubscribe_user(request):
    """Add user hash to unsubscribe list."""
    email_hash = request.GET.get('id')
    if not (request.method == 'GET' and email_hash):
        raise Http404
    unsubscribe.add(email_hash)
    return render(request, 'generic.html', {
        'title': "Unsubscribe successful",
        'message': ("You will no longer receive marketing emails from Galaxy"
                    " Australia."),
    })


def custom_400(request, exception, template_name="400.html"):
    """Custom view to show error messages."""
    return render(request, template_name, {
        'exc': exception,
    }, status=400)


def embed_snippet(request, snippet_path):
    """Serve an embeddable snippet."""
    ALLOW_STYLE_PARAMS = ['overflow']
    body_style_data = {
        k: request.GET.get(k)
        for k in ALLOW_STYLE_PARAMS
        if k in request.GET
    }
    body_style = ' '.join(
        f'{k}: {v};'
        for k, v in body_style_data.items()
    )
    try:
        if 'snippets' not in snippet_path:
            raise Http404
        return render(request, 'embed-snippet.html', {
            'title': 'Galaxy Media - embedded snippet',
            'snippet_path': snippet_path,
            # Can be referenced in snippet templates:
            'crop_margin': request.GET.get(
                'crop',
                'true',
            ).lower() in ('true', '1', 'yes'),
            'body_style': body_style,
        })
    except TemplateDoesNotExist:
        raise Http404
