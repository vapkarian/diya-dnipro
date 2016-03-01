from diya_dnipro.misc.models import SiteSetting


def social_icons(request):
    """
    Cached social links for header and footer.

    :param django.http.HttpRequest request: metadata about request
    :rtype: dict
    """
    return {
        'vkontakte_url': SiteSetting.get_value('vkontakte_url', '#'),
        'facebook_url': SiteSetting.get_value('facebook_url', '#'),
        'mail_url': SiteSetting.get_value('mail_url', '#'),
    }
