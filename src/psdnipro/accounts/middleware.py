from psdnipro.accounts.tasks import parse_tracking_info


__all__ = [
    'TrackingMiddleware',
]


class TrackingMiddleware(object):
    """
    Store UTM information received from referrers.
    """

    def process_request(self, request):
        """
        Save UTM information from GET parameters or cookies.

        :param django.http.HttpRequest request: metadata about request
        """
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
