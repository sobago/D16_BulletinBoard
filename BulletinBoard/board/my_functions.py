from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


def email_new_response(data):
    """email_new_response(data)\n
    data = object AdResponse """
    recipient = data.recipient
    current_site = Site.objects.get_current()
    html_content = render_to_string(
        'email_response_new.html', {
            "data": data,
            "recipient": recipient.username,
            "domain": current_site.domain
        }
    )
    email_i = [recipient.email]
    msg = EmailMultiAlternatives(
        subject=f'Новый отклик на объявление #{data.ad.id}',
        body=data.title,
        from_email='django_test123@sobago.ru',
        to=email_i,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def email_ad_response(data):
    recipient = data.sender
    current_site = Site.objects.get_current()
    html_content = render_to_string(
        'email_ad_response.html', {
            "data": data,
            "recipient": recipient.username,
            "domain": current_site.domain
        }
    )
    email_i = [recipient.email]
    msg = EmailMultiAlternatives(
        subject=f'Ответ на Ваш отклик по объявлению #{data.ad.id}',
        body=data.title,
        from_email='django_test123@sobago.ru',
        to=email_i,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# def email_to_subscribers(data):
#     recipient = data.sender
#     current_site = Site.objects.get_current()
#     html_content = render_to_string(
#         'email_ad_response.html', {
#             "data": data,
#             "recipient": recipient.username,
#             "domain": current_site.domain
#         }
#     )
#     email_i = [recipient.email]
#     msg = EmailMultiAlternatives(
#         subject=f'Ответ на Ваш отклик по объявлению #{data.ad.id}',
#         body=data.title,
#         from_email='django_test123@sobago.ru',
#         to=email_i,
#     )
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
