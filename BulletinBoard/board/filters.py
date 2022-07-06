import django.forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter

from accounts.models import MyUser
from .models import Ad, Category, AdResponse


def responses(request):
    if request is None:
        return Ad.objects.none()
    user = request.user
    return Ad.objects.filter(create_user=request.user.id)


class ResponsesFilter(FilterSet):

    ad = ModelChoiceFilter(
        field_name='ad',
        queryset=responses,
        label='Объявление',
        empty_label='Любые'
    )

