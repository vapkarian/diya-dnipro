from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from diya_dnipro.news.models import *


__all__ = [
    'CategorySectionSitemap', 'ArticleSitemap', 'TeamMemberSitemap',
]


class CategorySectionSitemap(Sitemap):
    priority = 0.4

    def items(self):
        items = []
        views = ('category', 'team', 'documents')
        for category in Category.objects.all():
            for view in views:
                items.append({'name': view, 'url': category.url})
        return items

    def location(self, obj):
        return reverse('news:{name}'.format(name=obj['name']), kwargs={'url': obj['url']})


class ArticleSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Article.objects.filter(is_active=True)

    @staticmethod
    def lastmod(obj):
        return obj.created


class TeamMemberSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return TeamMember.objects.filter(categories__isnull=False).distinct().order_by('id')
