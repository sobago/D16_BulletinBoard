from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', AdList.as_view(), name='ads'),
    path('<int:pk>/', AdDetail.as_view(), name='ad'),
    path('<int:pk>/edit/', AdUpdate.as_view(), name='ad_edit'),
    path('create/', login_required(AdCreate.as_view()), name='ad_create'),
    path('send_emails/', login_required(send_emails), name='send_emails'),
    path('<int:pk>/delete/', login_required(AdDelete.as_view()), name='ad_delete'),
    path('<int:pk>/response/', login_required(ad_response), name='ad_response'),
    path('responses/', login_required(AdResponses.as_view()), name='ad_responses'),
    path('responses/<int:pk>/', login_required(AdResponseView.as_view()), name='ad_response_detail'),
    path('responses/<int:pk>/accept/', login_required(response_accept), name='ad_response_accept'),
    path('responses/<int:pk>/refuse/', login_required(response_refuse), name='ad_response_refuse'),
]
