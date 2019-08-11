from django.conf import settings
from django.core import mail
from django.template import loader

from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from base64 import decodestring


def send_email(destination, subject, template, **kwargs):
    """ Sends an html email to the given receiver using the provided html template and name """

    # Make sure that destionation is a list
    if not isinstance(destination, list):
        destination = [destination]

    # Render the email template into html
    html = loader.render_to_string(template, context=kwargs)

    # Create an email message
    email = _create_email_message(
        subject, html, settings.EMAIL_FROM, destination)
    return email.send()


def _create_email_message(subject, html, from_email, recipient_list):
    """ Creates a connection for the email to be sent """

    # Extract images out of the email
    htmlcontent, images = _extract_images(html)

    # Make a connection to send the email via
    connection = mail.get_connection(
        username=None, password=None, fail_silently=False)

    # Create the html part of the email
    html_part = MIMEMultipart(_subtype='related')
    html_part.attach(MIMEText(htmlcontent, _subtype='html'))
    for image in images:
        html_part.attach(image)

    # create the plain text email and attach the html
    email = EmailMessage(subject, '', from_email,
                         recipient_list, connection=connection)
    email.attach(html_part)

    # and return the email
    return email


BASE_64_STRING = 'data:image/png;base64,'


def _extract_images(html):
    soup = BeautifulSoup(html, features='lxml')
    images = []

    counter = 0
    for img in soup.findAll('img'):
        src = img['src']
        if src.startswith(BASE_64_STRING):
            # generate a new cid
            cid = 'image' + str(counter)
            counter = counter + 1

            # Make the image
            image = _make_base64_image(src[len(BASE_64_STRING):], cid)
            images.append(image)

            # set the image attribute
            img['src'] = 'cid:' + cid

    return str(soup), images


def _make_base64_image(image, cid):
    """ Generates a single new image from a base64 string """
    img = MIMEImage(decodestring(bytes(image, 'ascii')), 'png')
    img.add_header('Content-Id', '<{}>'.format(cid))
    # David Hess recommended this edit
    img.add_header('Content-Disposition', 'inline',
                   filename='{}.png'.format(cid))
    return img
