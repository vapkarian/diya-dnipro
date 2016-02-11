from psdnipro.misc.models import SiteSetting

from psdnipro.news.models import Category, Article


__all__ = [
    'navigation_links', 'last_articles', 'top_articles', 'google_map',
]


def navigation_links(request):
    """
    List of categories for header navigation bar.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'navigation_links': Category.objects.filter(is_active=True).order_by('id')}


def last_articles(request):
    """
    List of last articles for all-news section.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'last_articles': Article.objects.filter(is_active=True, is_top=False).order_by('-created')[:5]}


def top_articles(request):
    """
    List of top articles for TOP slide-bar.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'top_articles': Article.objects.filter(is_active=True, is_top=True).order_by('-created')[:4]}


def google_map_url(request):
    """
    Cached google map for contacts page.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {
        'google_map_url': SiteSetting.get_value('google_map_url', '#'),
    }
