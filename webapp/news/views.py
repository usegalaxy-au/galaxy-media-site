"""News views."""

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import News


def index(request):
    """Show news list page."""
    news_items = News.objects.filter(is_tool_update=False)
    if not request.user.is_staff:
        news_items = news_items.filter(is_published=True)
    return render(request, 'news/index.html', {
        'news_items': news_items.order_by('-datetime_created'),
    })


def show(request, pk=None):
    """Show news article page."""
    try:
        return render(request, 'news/article.html', {
            'article': News.objects.get(id=pk),
        })
    except ObjectDoesNotExist:
        raise Http404
