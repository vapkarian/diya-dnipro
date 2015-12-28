from django.contrib import admin
from psdnipro.news.models import *


__all__ = [
    'CategoryAdmin', 'ArticleAdmin', 'TeamMemberAdmin', 'DocumentAdmin',
]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active')
    list_filter = ('is_active',)
    ordering = ('id',)
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.news.models.Category obj: instance
        :rtype bool
        """
        return False


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created', 'is_top', 'is_active')
    list_filter = ('is_active', 'is_top')
    list_select_related = ('category',)
    ordering = ('-created',)
    search_fields = ('title', 'text')
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.news.models.Article obj: instance
        :rtype bool
        """
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'is_active')
    list_filter = ('is_active', 'category')
    list_select_related = ('category',)
    ordering = ('id',)
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.news.models.TeamMember obj: instance
        :rtype bool
        """
        return False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'clickable_url', 'category', 'is_active')
    list_filter = ('is_active', 'category')
    list_select_related = ('category',)
    ordering = ('id',)
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.news.models.Document obj: instance
        :rtype bool
        """
        return False

    def clickable_url(self, obj):
        """
        Link to the document.

        :param psdnipro.news.models.Document obj: instance
        :rtype bool
        """
        return '<a href="{url}">{title}</a>'.format(url=obj.url, title=obj.title)

    clickable_url.allow_tags = True
    clickable_url.description = 'Посилання'
