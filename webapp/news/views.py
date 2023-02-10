"""News views."""

from django.shortcuts import get_object_or_404, render

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
    if request.user.is_staff:
        article = get_object_or_404(
            News,
            id=pk,
        )
    else:
        article = get_object_or_404(
            News,
            id=pk,
            is_published=True,
        )
    return render(request, 'news/article.html', {
        'article': article,
    })
