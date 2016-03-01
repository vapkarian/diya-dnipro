from django.conf.urls import url
from diya_dnipro.news.views import *


__all__ = [
    'urlpatterns',
]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^category/(?P<url>.+)/$', CategoryView.as_view(), name='category'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^article/(?P<pk>\d+)/$', ArticleView.as_view(), name='article'),
    url(r'^team/(?P<url>.+)/$', TeamView.as_view(), name='team'),
    url(r'^member/(?P<pk>\d+)/$', TeamMemberView.as_view(), name='member'),
    url(r'^documents/(?P<url>.+)/$', DocumentsView.as_view(), name='documents'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
]
