from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(('E-mail'), unique=True, help_text='Обязательное поле, Ваша электронная почта.')
    REQUIRED_FIELDS = ['username', ]
    subscriber = models.BooleanField(
        ("Статус подписки на новости"),
        default=True,
    )
