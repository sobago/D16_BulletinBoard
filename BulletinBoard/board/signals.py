from django.db.models.signals import post_save
from django.dispatch import receiver
from board.my_functions import email_new_response
from board.models import AdResponse


# @receiver(post_save, sender=AdResponse)
# def notify_new_post(sender, instance, **kwargs):
#     email_new_response(instance)
