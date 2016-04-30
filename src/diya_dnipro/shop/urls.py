from django.conf.urls import url

from diya_dnipro.shop.views import *


__all__ = [
    'urlpatterns',
]

urlpatterns = [
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^category/(?P<url>.+)/$', CategoryView.as_view(), name='category'),
    url(r'^item/(?P<pk>\d+)/$', ItemView.as_view(), name='item'),

]
