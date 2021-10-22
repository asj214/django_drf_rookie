from django.urls import path
from .views import (
    LoginView,
    AuthMeView,
)


urlpatterns = [
    path(r'auth/login', LoginView.as_view()),
    path(r'auth/me', AuthMeView.as_view()),
]
