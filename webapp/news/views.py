"""News views."""

from django.shortcuts import render

from .models import News


def index(request):
    """Show news list page."""
    return render(request, 'news/index.html', {
        'news_items': News.objects.order_by('datetime_created'),
    })
