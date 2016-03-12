from django.http import HttpRequest

from diya_dnipro.misc.models import SiteSetting
from diya_dnipro.news.models import Category, Article


__all__ = [
    'navigation_links', 'last_articles', 'top_articles', 'google_map',
]


def navigation_links(request: HttpRequest) -> dict:
    """
    List of categories for header navigation bar.
    """
    return {'navigation_links': Category.objects.order_by('id')}


def last_articles(request: HttpRequest) -> dict:
    """
    List of last articles for all-news section.
    """
    return {'last_articles': Article.objects.filter(is_active=True, is_top=False).order_by('-created')[:5]}


def top_articles(request: HttpRequest) -> dict:
    """
    List of top articles for TOP slide-bar.
    """
    return {'top_articles': Article.objects.filter(is_active=True, is_top=True).order_by('-created')[:4]}


def google_map_url(request: HttpRequest) -> dict:
    """
    Cached google map for contacts page.
    """
    return {
        'google_map_url': SiteSetting.get_value('google_map_url', '#'),
    }
