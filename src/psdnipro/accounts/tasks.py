from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from psdnipro import celery_app


__all__ = [
    'send_mail',
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
