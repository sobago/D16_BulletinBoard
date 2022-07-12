from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import ResponsesFilter
from .forms import AdDetailForm, AdResponseForm, SendEmailsForm
from .models import *
from .my_functions import email_ad_response, email_new_response
from .tasks import email_to_subscribers


class AdList(ListView):
    model = Ad
    ordering = '-create_datetime'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 2

    def get_queryset(self):
        return Ad.objects.all().select_related("category")


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            ad_resp = AdResponse.objects.get(ad=self.object, sender=self.request.user)
            if ad_resp:
                context['ad_resp'] = ad_resp
        except AdResponse.DoesNotExist:
            context['ad_resp'] = False
        return context

    def get_queryset(self):
        return Ad.objects.all().select_related("category")


class AdUpdate(UpdateView):
    form_class = AdDetailForm
    model = Ad
    template_name = 'ad_edit.html'


class AdCreate(CreateView):
    form_class = AdDetailForm
    model = Ad
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.create_user = self.request.user
        return super().form_valid(form)


class AdDelete(DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ads')


class AdResponseView(DetailView):
    model = AdResponse
    template_name = 'ad_response_detail.html'
    context_object_name = 'response'


class AdResponses(ListView):
    model = AdResponse
    template_name = 'ad_responses.html'
    context_object_name = 'responses'
    ordering = '-create_datetime'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(recipient=self.request.user)
        self.filterset = ResponsesFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def ad_response(request, pk):
    """Форма отклика на объявление, получает request и id объявления"""
    form = AdResponseForm(request.POST or None)
    if request.method == 'POST':
        form = AdResponseForm(request.POST)
        if form.is_valid():
            ad = Ad.objects.get(id=pk)
            resp = AdResponse.objects.create(
                title=form.cleaned_data['title'],
                sender=request.user,
                recipient=ad.create_user,
                ad=ad
            )
            email_new_response(resp)
            return HttpResponseRedirect(reverse_lazy('ad', kwargs={'pk': pk}))
        else:
            form = AdResponseForm()

    return render(request, 'ad_response.html', {'form': form, 'pk': pk})


def send_emails(request):
    """Отправка email подписчикам"""
    form = SendEmailsForm(request.POST or None)
    if request.user.is_staff:
        if request.method == 'POST':
            form = SendEmailsForm(request.POST)
            if form.is_valid():
                form.cleaned_data['text'] = replace_relatve_path_with_absolute_url(form.cleaned_data['text'])
                for user in MyUser.objects.filter(subscriber=True):
                    email_to_subscribers(form.cleaned_data, user.email)
                return HttpResponseRedirect('/')

            else:
                form = SendEmailsForm()

        return render(request, 'send_emails.html', {'form': form})
    else:
        raise PermissionDenied('Доступ только для персонала')


def replace_relatve_path_with_absolute_url(message):
    """Замена ссылки с вложениями для email-рассылок на полный путь"""
    search = settings.MEDIA_URL + settings.CKEDITOR_UPLOAD_PATH
    current_site = str(Site.objects.get_current())
    message = message.replace(search, current_site + search)
    return message


def response_accept(request, pk):
    """Одобрение отклика"""
    user = request.user
    adresp = AdResponse.objects.get(pk=pk)
    if adresp.recipient == user:
        adresp.is_accepted = True
        adresp.is_refused = False
        adresp.save()
        email_ad_response(adresp)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise PermissionDenied('Отклик принадлежит другому пользователю')


def response_refuse(request, pk):
    """Отказ от отклика"""
    user = request.user
    adresp = AdResponse.objects.get(pk=pk)
    if adresp.recipient == user:
        adresp.is_accepted = False
        adresp.is_refused = True
        adresp.save()
        email_ad_response(adresp)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise PermissionDenied('Отклик принадлежит другому пользователю')

