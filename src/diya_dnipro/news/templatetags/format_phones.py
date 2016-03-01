from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def format_phones(value):
    """
    Transform phones into comma-separated framed phones with tel: schema.

    :param str value: comma-separated string line of phone numbers
    :rtype str
    """
    phones = value.split(',')
    phones = [
        '<a href="tel:{formatted_phone}">{phone}</a>'.format(
            formatted_phone=''.join(filter(lambda x: x.isdigit(), phone)),
            phone=phone.strip()
        ) for phone in phones]
    return mark_safe(', '.join(phones))
