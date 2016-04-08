from django import template
from django.template import RequestContext


register = template.Library()


@register.simple_tag(takes_context=True)
def add_host(context: RequestContext) -> str:
    """
    Provide host with protocol (either "http" or "https") for creating absolute url if it's possible.
    """
    request = context.get('request')
    if request is not None:
        return '%s://%s' % (request.scheme, request.get_host())
    return ''
