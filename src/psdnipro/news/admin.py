from django.contrib import admin
from psdnipro.news.models import Image, Category, Article, TeamMember


__all__ = [
    'ImageAdmin', 'CategoryAdmin', 'ArticleAdmin',
]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'preview', 'note')
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.news.models.Image obj: instance
        :rtype bool
        """
        return False


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
    fieldsets = (
        ('Основна інформація', {'fields': ('title', 'category', ('main_image', 'main_image_preview'), 'text',
                                           'images', 'images_previews')}),
        ('Додаткова інформация', {'fields': ('created', 'is_active')}),
        ('Інформация про ТОП', {'fields': ('is_top', ('top_image', 'top_image_preview'))}),
    )
    list_display = ('title', 'category', 'created', 'is_top', 'is_active')
    list_filter = ('is_top', 'is_active')
    list_select_related = ('category',)
    ordering = ('-created',)
    raw_id_fields = ('images', 'main_image', 'top_image')
    readonly_fields = ('main_image_preview', 'top_image_preview', 'images_previews')
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

    def main_image_preview(self, obj):
        """
        Generate preview image tag for main image.

        :param psdnipro.news.models.Article obj: instance
        :rtype bool
        """
        if obj.main_image is not None:
            return obj.main_image.preview

    main_image_preview.allow_tags = True
    main_image_preview.short_description = 'Попередній перегляд'

    def top_image_preview(self, obj):
        """
        Generate preview image tag for top image.

        :param psdnipro.news.models.Article obj: instance
        :rtype bool
        """
        if obj.top_image is not None:
            return obj.top_image.preview

    top_image_preview.allow_tags = True
    top_image_preview.short_description = 'Попередній перегляд'

    def images_previews(self, obj):
        """
        Generate preview image tags for all images.

        :param psdnipro.news.models.Article obj: instance
        :rtype bool
        """
        return ''.join(elem.preview for elem in obj.images.all())

    images_previews.allow_tags = True
    images_previews.short_description = 'Попередній перегляд'


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
        :param psdnipro.news.models.Category obj: instance
        :rtype bool
        """
        return False
