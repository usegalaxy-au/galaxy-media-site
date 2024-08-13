"""Views for home app."""

import os
import logging
import pprint
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import (
    RequestContext,
    loader,
    Template,
    TemplateDoesNotExist,
)
from django.template.loader import get_template, render_to_string

from events.models import Event
from news.models import News
from utils import aaf
from utils import unsubscribe
from utils.exceptions import ResourceAccessError, SubsiteBuildError
from .lab_cache import LabCache
from .lab_export import ExportSubsiteContext
from .models import CoverImage, Notice
from .forms import (
    ResourceRequestForm,
    QuotaRequestForm,
    SupportRequestForm,
    ACCESS_FORMS,
)
from . import pages_context
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
        'cover_image': CoverImage.get_random(request),
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

    context = {
        'extend_template': 'home/header.html',
        'export': False,
        'name': subdomain,
        'site_name': settings.GALAXY_SITE_NAME,
        'nationality': 'Australian',
        'galaxy_base_url': settings.GALAXY_URL,
    }
    if request.GET.get('export'):
        context = ExportSubsiteContext(request)
        context.validate()
        context.update({
            'name': subdomain,
            'title': f'Galaxy - {subdomain.title()} Lab',
        })
        if not context.get('sections'):
            context['sections'] = sections
    else:
        context.update({
            'sections': sections,
            'notices': Notice.get_notices_by_type(request, subsite=subdomain),
            'cover_image': CoverImage.get_random(request, subsite=subdomain),
            'form': SupportRequestForm(),
        })

    response = render(request, template, context)
    response.content = response.content.replace(
        b'{{ galaxy_base_url }}',
        context['galaxy_base_url'].encode('utf-8'))
    return response


def export_lab(request):
    """Generic Galaxy Lab landing page build with externally hosted content.

    These pages are built on the fly and can be requested by third parties on
    an ad hoc basis, where the content would typically be hosted in a GitHub
    repo with a YAML file root which is specified as a GET parameter.
    """

    if response := LabCache.get(request):
        return response

    template = 'home/subdomains/exported.html'

    try:
        if request.GET.get('content_root'):
            context = ExportSubsiteContext(request.GET.get('content_root'))
        else:
            context = ExportSubsiteContext(
                settings.DEFAULT_EXPORTED_LAB_CONTENT_ROOT)
        context['HOSTNAME'] = settings.HOSTNAME
        context.validate()
    except SubsiteBuildError as exc:
        return render(request, 'home/subdomains/export-error.html', {
            'exc': exc,
        }, status=400)

    # Multiple rounds of templating to render recursive template tags from
    # remote data with embedded template tags
    i = 0
    prev_template_str = ''
    template_str = render_to_string(template, context, request)
    while prev_template_str.strip('\n') != template_str.strip('\n') and i < 4:
        prev_template_str = template_str
        t = Template('{% load markdown %}\n\n' + template_str)
        template_str = t.render(RequestContext(request, context))
        i += 1

    response = LabCache.put(request, template_str)

    return response


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
    try:
        if 'snippets' not in snippet_path:
            raise Http404
        return render(request, 'embed-snippet.html', {
            'title': 'Galaxy Media - embedded snippet',
            'snippet_path': snippet_path,
        })
    except TemplateDoesNotExist:
        raise Http404
