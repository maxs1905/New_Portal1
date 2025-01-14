from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    path('signup/',
         BaseRegisterView.as_view(template_name = 'sign/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]