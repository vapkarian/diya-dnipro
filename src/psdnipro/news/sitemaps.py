from django.contrib.sitemaps import Sitemap

from psdnipro.news.models import Article, Category, TeamMember


__all__ = [
    'CategorySitemap', 'ArticleSitemap', 'TeamMemberSitemap',
]


class CategorySitemap(Sitemap):
    priority = 0.4

    def items(self):
        return Category.objects.all()


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
        return TeamMember.objects.all()
