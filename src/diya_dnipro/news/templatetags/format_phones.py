from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def format_phones(value: str) -> str:
    """
    Transform phones into comma-separated framed phones with tel: schema.
    """
    phones = value.split(',')
    phones = [
        '<a href="tel:{formatted_phone}">{phone}</a>'.format(
                formatted_phone=''.join(filter(lambda x: x.isdigit(), phone)),
                phone=phone.strip()
        ) for phone in phones]
    return mark_safe(', '.join(phones))
