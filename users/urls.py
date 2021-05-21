from django.urls import path
from .views import (RegisterUserView, LoginView, UserView)

urlpatterns = [
    path(r'auth/register', RegisterUserView.as_view()),
    path(r'auth/login', LoginView.as_view()),
    path(r'auth/me', UserView.as_view()),
]