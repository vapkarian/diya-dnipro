from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from psdnipro.accounts.forms import *
from psdnipro.accounts.models import *


__all__ = [
    'UserAdmin', 'FeedbackAdmin', 'TrackingRecordAdmin',
]


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Define and provide necessary admin options and functionality for a User model.
    """
    fieldsets = (
        ('Персональна інформація', {'fields': ('email', 'name', 'password')}),
        ('Права доступу', {'fields': ('is_active', 'is_beta', 'is_staff', 'is_superuser', 'groups',
                                      'user_permissions')}),
        ('Важливі дати', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2'), 'classes': ('wide',)}),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'name', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_beta', 'is_staff', 'is_superuser', 'is_superuser', 'groups')
    search_fields = ('name', 'email')
    ordering = ('-last_login',)
    filter_horizontal = ('groups', 'user_permissions',)
    save_on_top = True


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = ('email', 'message', 'created')
    list_display = ('email', 'preview', 'created')
    ordering = ('-created',)
    readonly_fields = ('email', 'message', 'created')
    save_on_top = True

    def has_add_permission(self, request, obj=None):
        """
        Prevent adding objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.accounts.models.Feedback obj: instance
        :rtype bool
        """
        return False

    def preview(self, obj):
        """
        First 120 symbols of message.

        :param psdnipro.news.models.Feedback obj: instance
        :rtype str
        """
        if len(obj.message) > 120:
            return '{}...'.format(obj.message[:117])
        return obj.message


@admin.register(TrackingRecord)
class TrackingRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Вихідна інформация', {'fields': ('ua_string', 'ip', 'referrer', 'created')}),
        ('Браузер', {'fields': ('browser_family', 'browser_version')}),
        ('Операційна система', {'fields': ('os_family', 'os_version')}),
        ('Пристрій', {'fields': ('device_brand', 'device_family', 'device_model')}),
        ('Місцезнаходження', {'fields': ('coordinates', 'city', 'region', 'country')}),
    )
    readonly_fields = (
        'ua_string', 'ip', 'referrer', 'browser_family', 'browser_version', 'os_family', 'os_version', 'device_brand',
        'device_family', 'device_model', 'coordinates', 'city', 'region', 'country', 'created', 'clickable_map_url',
    )
    list_display = ('ip', 'referrer', 'browser', 'os', 'device', 'clickable_map_url', 'created')
    list_filter = ('browser_family', 'os_family', 'device_brand', 'city', 'country')
    ordering = ('-created',)
    save_on_top = True

    def has_add_permission(self, request, obj=None):
        """
        Prevent adding objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.accounts.models.TrackingRecord obj: instance
        :rtype bool
        """
        return False

    def clickable_map_url(self, obj):
        """
        Link to google map.

        :param psdnipro.accounts.models.TrackingRecord obj: instance
        :rtype str
        """
        url = obj.map_url
        title = 'Карта'
        if url:
            return '<a href="{url}" target="_blank">{title}</a>'.format(url=url, title=title)
        return 'недоступно'

    clickable_map_url.allow_tags = True
    clickable_map_url.short_description = 'Карта'
