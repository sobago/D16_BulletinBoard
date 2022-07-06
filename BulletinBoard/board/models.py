from django.urls import reverse

from accounts.models import MyUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name='Наименование категории', unique=True)

    def __str__(self):
        return f'{self.title}'


class Ad(models.Model):
    title = models.CharField(max_length=254, verbose_name='Заголовок объявления')
    text = RichTextUploadingField(verbose_name='Текст объявления')
    create_datetime = models.DateTimeField(auto_now_add=True)
    create_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('ad', args=[str(self.pk)])

    def __str__(self):
        return f'{self.id} {self.title}'


class AdResponse(models.Model):
    title = models.CharField(max_length=254, verbose_name='Текст запроса')
    sender = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='+', verbose_name='Отправитель')
    recipient = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='+', verbose_name='Получатель')
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_refused = models.BooleanField(default=False)
