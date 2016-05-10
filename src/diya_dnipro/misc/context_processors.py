from django.conf import settings
from django.http import HttpRequest

from diya_dnipro.misc.models import SiteSetting


def social_icons(request: HttpRequest) -> dict:
    """
    Cached social links for header and footer.
    """
    return {
        'vkontakte_url': SiteSetting.get_value('vkontakte_url', '#'),
        'facebook_url': SiteSetting.get_value('facebook_url', '#'),
        'mail_url': SiteSetting.get_value('mail_url', '#'),
    }


def settings_constants(request: HttpRequest) -> dict:
    """
    All constants from project settings.
    """
    return {
        'settings': settings,
    }
