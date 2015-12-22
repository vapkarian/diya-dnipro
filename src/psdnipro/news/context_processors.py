from psdnipro.news.models import Category, Article


def navigation_links(request):
    """
    List of categories for header navigation bar.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'navigation_links': Category.objects.order_by('id')}


def last_articles(request):
    """
    List of last articles for all-news section.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'last_articles': Article.objects.filter(is_active=True).order_by('-created')[:5]}


def top_articles(request):
    """
    List of top articles for TOP slide-bar.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {'top_articles': Article.objects.filter(is_active=True, is_top=True).order_by('-created')[:4]}
