from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import requests
from ua_parser import user_agent_parser

from psdnipro import celery_app
from psdnipro.accounts.models import TrackingRecord


__all__ = [
    'send_mail', 'parse_tracking_info',
]


@celery_app.task
def send_mail(emails, subject, text_template, html_template=None, extra_context=None, attachments=None, reply_to=None):
    """
    Send email message.

    :param list[unicode] emails: list of email addresses
    :param unicode subject: subject of email
    :param dict extra_context: context of html/txt templates
    :param str text_template: path to the main text template
    :param str html_template: path to the alternative non-required html template
    :param list[tuple[str, object, str]] attachments: list of triples `filename` - `content` - `mimetype`
        for attachments
    :param tuple[str, str] reply_to: pair of name and email of `Reply-To` section
    """
    emails = [email for email in emails if bool(email)]
    if not emails:
        return
    sender = settings.DEFAULT_FROM_EMAIL
    headers = {}
    if reply_to is not None:
        reply_name, reply_email = reply_to
        sender = u'"{reply_name}" <{from_email}>'.format(reply_name=reply_name, from_email=settings.DEFAULT_FROM_EMAIL)
        headers['Reply-To'] = u'"{reply_name}" <{reply_email}>'.format(reply_name=reply_name, reply_email=reply_email)
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    text_content = get_template(text_template).render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=emails, headers=headers)
    if html_template is not None:
        html_content = get_template(html_template).render(context)
        msg.attach_alternative(html_content, 'text/html')
    if attachments is not None:
        for filename, content, mimetype in attachments:
            msg.attach(filename, content, mimetype)
    msg.send()


@celery_app.task
def parse_tracking_info(ua_string, ip, referrer):
    fields = {'ua_string': ua_string, 'ip': ip, 'referrer': referrer}

    if ua_string:
        ua_info = user_agent_parser.Parse(ua_string)
        fields['browser_family'] = ua_info['user_agent']['family']
        fields['browser_version'] = ua_info['user_agent']['major']
        fields['os_family'] = ua_info['os']['family']
        fields['os_version'] = ua_info['os']['major']
        fields['device_brand'] = ua_info['device']['brand']
        fields['device_family'] = ua_info['device']['family']
        fields['device_model'] = ua_info['device']['model']

    if ip:
        same_ip = TrackingRecord.objects.filter(ip=ip).last()
        if same_ip is not None:
            fields['coordinates'] = same_ip.coordinates
            fields['city'] = same_ip.city
            fields['region'] = same_ip.region
            fields['country'] = same_ip.country
        else:
            response = requests.get('http://ipinfo.io/{}'.format(ip))
            ip_info = response.json()
            fields['coordinates'] = ip_info.get('loc')
            fields['city'] = ip_info.get('city')
            fields['region'] = ip_info.get('region')
            fields['country'] = ip_info.get('country')

    fields = {key: value or '' for key, value in fields.items()}
    TrackingRecord.objects.create(**fields)
