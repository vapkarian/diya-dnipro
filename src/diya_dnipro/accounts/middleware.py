from typing import Callable

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from diya_dnipro.accounts.tasks import parse_tracking_info


__all__ = [
    'TrackingMiddleware', 'BetaTestingMiddleware',
]


class TrackingMiddleware(object):
    """
    Store UTM information received from referrers.
    """

    def process_request(self, request: HttpRequest) -> None:
        if 'tracked' in request.session:
            return

        ua_string = request.META.get('HTTP_USER_AGENT')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        referrer = request.META.get('HTTP_REFERER')

        parse_tracking_info.delay(ua_string, ip, referrer)
        request.session['tracked'] = True


class BetaTestingMiddleware(object):
    """
    Allow view only for beta users.
    """

    def process_view(self, request: HttpRequest, view_func: Callable, view_args: list, view_kwargs: dict):
        if view_kwargs.get('beta_testing', False) and not getattr(request.user, 'is_beta', False):
            raise PermissionDenied
