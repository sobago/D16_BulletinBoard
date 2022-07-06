from celery import shared_task
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def email_to_subscribers(data, email):
    current_site = Site.objects.get_current()
    html_content = render_to_string(
        'email_to_subscribers.html', {
            "data": data,
            "domain": current_site.domain
        }
    )
    msg = EmailMultiAlternatives(
        subject=f"{data['subject']}",
        body=data['text'],
        from_email='django_test123@sobago.ru',
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

