from psdnipro.news.sitemaps import *


__all__ = [
    'SITEMAPS',
]

SITEMAPS = {
    'categories': CategorySitemap(),
    'articles': ArticleSitemap(),
    'team_members': TeamMemberSitemap(),
}
