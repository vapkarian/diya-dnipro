from django.contrib import admin
from psdnipro.misc.models import SiteSetting


__all__ = [
    'SiteSettingAdmin',
]


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'type', 'value', 'description')
    list_editable = ('value',)
    list_filter = ('section',)
    ordering = ('section', 'key')
    save_on_top = True
