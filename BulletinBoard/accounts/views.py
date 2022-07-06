from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import MyUser
from .forms import UserForm


class ProfileDetail(DetailView):
    model = MyUser
    template_name = 'profile_detail.html'
    context_object_name = 'profile_detail'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = MyUser
    template_name = 'profile_edit.html'
    success_url = '/'
