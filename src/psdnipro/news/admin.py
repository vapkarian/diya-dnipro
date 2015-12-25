from django.contrib import admin
from psdnipro.news.models import Category, Article, TeamMember


__all__ = [
    'CategoryAdmin', 'ArticleAdmin', 'TeamMemberAdmin',
]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
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
    list_filter = ('is_top', 'is_active')
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
    list_display = ('name', 'position', 'category')
    list_filter = ('category',)
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
