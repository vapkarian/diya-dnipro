from django.conf.urls import url
from psdnipro.news.views import HomeView, CategoryView, ArticleView

__all__ = [
    'urlpatterns',
]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^category/(?P<url>.+)/$', CategoryView.as_view(), name='category'),
    url(r'^article/(?P<pk>\d+)/$', ArticleView.as_view(), name='article'),
]
