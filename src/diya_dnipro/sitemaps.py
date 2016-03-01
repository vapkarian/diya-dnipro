from diya_dnipro.news.sitemaps import *


__all__ = [
    'SITEMAPS',
]

SITEMAPS = {
    'categories': CategorySectionSitemap(),
    'articles': ArticleSitemap(),
    'team_members': TeamMemberSitemap(),
}
