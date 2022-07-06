from django.contrib.auth import views
from django.urls import path, include
from django_registration.forms import RegistrationFormUniqueEmail
from django_registration.backends.activation import views as reg_views
from django.views.generic.base import TemplateView
from .forms import MyCustomUserForm
from .views import ProfileDetail, ProfileUpdate

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', reg_views.RegistrationView.as_view(form_class=MyCustomUserForm), name='django_registration_register'),
    path('activate/complete/',
         TemplateView.as_view(template_name="django_registration/activation_complete.html"),
         name="django_registration_activation_complete",
         ),
    path("activate/<str:activation_key>/",
         reg_views.ActivationView.as_view(),
         name="django_registration_activate",
         ),
    path("register/complete/",
         TemplateView.as_view(template_name="django_registration/registration_complete.html"),
         name="django_registration_complete",
         ),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('profile/<int:pk>/edit', ProfileUpdate.as_view(), name='profile_update'),
]


# urlpatterns = patterns('',
#     url(r'^register/$',
#         RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
#         name='registration_register'),
# )

