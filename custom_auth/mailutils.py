from django.conf import settings
from django.core import mail
from django.utils.html import strip_tags
from django.template import loader

def send_email(destination, subject, template, **kwargs):
    """ Sends an html email to the given receiver using the provided html template and name """

    # Make sure that destionation is a list
    if not isinstance(destination, list):
        destination = [destination]

    # Render the email template into html and also re-create a plain version
    html = loader.render_to_string(template, context=kwargs)
    txt = strip_tags(html)

    # and then send the email
    return mail.send_mail(subject, txt, settings.EMAIL_FROM, destination, html_message=html)