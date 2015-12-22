from django.conf.urls import url
from psdnipro.news.views import HomeView, CategoryView, ArticleView, TeamView, TeamMemberView


__all__ = [
    'urlpatterns',
]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^news/(?P<url>.+)/$', CategoryView.as_view(), name='news'),
    url(r'^team/(?P<url>.+)/$', TeamView.as_view(), name='team'),
    url(r'^article/(?P<pk>\d+)/$', ArticleView.as_view(), name='article'),
    url(r'^member/(?P<pk>\d+)/$', TeamMemberView.as_view(), name='member'),
]
