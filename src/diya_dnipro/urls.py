"""diya_dnipro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from diya_dnipro.sitemaps import SITEMAPS


admin.site.site_header = admin.site.site_title = 'Файна адмінка'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='misc/robots.txt', content_type='text/plain'),
        name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    url(r'^', include('diya_dnipro.news.urls', namespace='news')),
    url(r'^shop/', include('diya_dnipro.shop.urls', namespace='shop'), {'beta_testing': True}),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
