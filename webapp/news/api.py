"""API for interacting with News items."""

from datetime import date
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils.notifications import notify_tool_update
from events.models import Tag, Supporter
from .models import News, APIToken


@csrf_exempt
def create_post(request):
    """Create a new post.

    To post a tool update:

    curl -X POST -d "api_token=<token>
        &tool_update=true
        &body=$(cat body.txt)"
        http://127.0.0.1:5000/news/api/create
    """
    if request.method == 'GET':
        return HttpResponse(
            f'{request.get_host()} News post API\n'
            'POST requests take the following parameters:\n'
            '------------------------------------\n'
            'api_token:    [REQUIRED] Authenticate with the server\n'
            'body:         [REQUIRED] Body of the post in markdown format\n'
            'title:        Title of the post to create.'
            ' Required if not tool update.\n'
            'tool_update:  If tool update, title created automatically'
            ' (true/false)\n',
            content_type="text/plain"
        )

    if request.method != "POST":
        return HttpResponse(
            "Bad request: HTTP method not allowed",
            content_type="text/plain",
            status=400,
        )
    if not APIToken.objects.count():
        return HttpResponse(
            (
                'Sorry, the server has not been configured for API access.'
                ' Only an administrator of this application can enable API'
                ' requests.\n'
            ),
            status=401,
            content_type="text/plain"
        )
    if not APIToken.matches(request.POST.get('api_token')):
        return HttpResponse(
            "Authentication failed\n",
            status=401,
            content_type="text/plain"
        )

    title = request.POST.get('title')
    body = request.POST.get('body')
    tool_update = request.POST.get('tool_update').lower() == 'true'
    if tool_update:
        today = date.today().strftime('%Y-%m-%d')
        title = f"Galaxy {settings.GALAXY_SITE_NAME} Tool Update {today}"
    if not body:
        return HttpResponse(
            'Bad request: "body" field is required\n.',
            content_type="text/plain",
            status=400,
        )
    if not title:
        return HttpResponse(
            'Bad request: "title" field is required\n.',
            content_type="text/plain",
            status=400,
        )

    body_markdown = [x for x in body.split('---\n', 2) if x][1].strip(' \n')
    article = News.objects.create(
        title=title,
        body=body_markdown,
        is_published=True,
        is_tool_update=tool_update,
    )
    tags = Tag.objects.filter(name="tools")
    supporters = Supporter.objects.filter(
        name__in=["Galaxy Australia", "QCIF", "Melbourne Bioinformatics"]
    )
    for tag in tags:
        article.tags.add(tag)
    for supporter in supporters:
        article.supporters.add(supporter)

    if tool_update:
        notify_tool_update(article)

    return HttpResponse(
        'News item created successfully\n',
        status=201,
        content_type="text/plain"
    )
