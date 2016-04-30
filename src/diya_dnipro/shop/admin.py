from django.contrib import admin

from diya_dnipro.shop.models import *


__all__ = [
    'CategoryAdmin',
]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'image')
    list_display = ('title', 'url')
    list_filter = ()
    ordering = ('id',)
    save_on_top = True


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
