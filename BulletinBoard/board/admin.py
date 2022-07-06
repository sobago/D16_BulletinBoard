from django.contrib import admin
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

#
# class AdAdminForm(forms.ModelForm):
#     text = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Ad
#         fields = '__all__'


class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    # form = AdAdminForm


class AdResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ad')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(AdResponse, AdResponseAdmin)
