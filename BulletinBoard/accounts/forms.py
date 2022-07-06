from django_registration.forms import RegistrationForm
from .models import MyUser
from django import forms


class MyCustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = MyUser

        fields = [
            MyUser.USERNAME_FIELD,
            'username',
            "password1",
            "password2",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'subscriber',
        ]
