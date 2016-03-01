from django.contrib import admin
from diya_dnipro.news.models import *


__all__ = [
    'CategoryAdmin', 'ArticleAdmin', 'TeamMemberAdmin', 'DocumentAdmin', 'ContactAdmin',
]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'members', 'documents')
    list_display = ('title', 'url')
    list_filter = ()
    ordering = ('id',)
    save_on_top = True


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created', 'is_top', 'is_active')
    list_filter = ('is_active', 'is_top')
    list_select_related = ('category',)
    ordering = ('-created',)
    search_fields = ('title', 'text')
    save_on_top = True


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    list_filter = ('categories',)
    ordering = ('id',)
    save_on_top = True


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'clickable_url')
    list_filter = ('categories', )
    ordering = ('id',)
    save_on_top = True

    def clickable_url(self, obj):
        """
        Link to the document.

        :param diya_dnipro.news.models.Document obj: instance
        :rtype str
        """
        return '<a href="{url}" target="_blank">{title}</a>'.format(url=obj.url, title=obj.title)

    clickable_url.allow_tags = True
    clickable_url.description = 'Посилання'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'phones')
    list_filter = ()
    ordering = ('id',)
    save_on_top = True
