from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from psdnipro.accounts.forms import *
from psdnipro.accounts.models import *


__all__ = [
    'UserAdmin', 'FeedbackAdmin',
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

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting objects by admins.

        :param django.http.HttpRequest request: metadata about request
        :param psdnipro.accounts.models.User obj: instance
        :rtype bool
        """
        return False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = ('email', 'message', 'created')
    list_display = ('email', 'preview', 'created')
    ordering = ('-created',)

    def preview(self, obj):
        """
        First 120 symbols of message.

        :param psdnipro.news.models.Feedback obj: instance
        :rtype str
        """
        if len(obj.message) > 120:
            return '{}...'.format(obj.message[:117])
        return obj.message
