"""News views."""

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import News


def index(request):
    """Show news list page."""
    return render(request, 'news/index.html', {
        'news_items': News.objects.order_by('-datetime_created'),
    })


def show(request, pk=None):
    """Show news article page."""
    try:
        return render(request, 'news/article.html', {
            'article': News.objects.get(id=pk),
        })
    except ObjectDoesNotExist:
        raise Http404
