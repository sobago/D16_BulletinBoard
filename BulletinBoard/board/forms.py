from django import forms
from board.models import Ad, AdResponse
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdDetailForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget, label='Текст объявления')

    class Meta:
        model = Ad
        fields = [
            'title',
            'text',
            'category',
        ]


class AdResponseForm(forms.ModelForm):

    class Meta:
        model = AdResponse
        fields = [
            'title',
        ]


class SendEmailsForm(forms.Form):
    subject = forms.CharField(max_length=128, label='Заголовок письма')
    text = forms.CharField(widget=CKEditorUploadingWidget, label='Текст рассылки')


