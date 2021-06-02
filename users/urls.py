from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUserView,
    LoginView,
    UserView,
    ReGenerateTokenView,
    UserViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'auth/register', RegisterUserView.as_view()),
    path(r'auth/login', LoginView.as_view()),
    path(r'auth/me', UserView.as_view()),
    path(r'auth/access_token', ReGenerateTokenView.as_view()),
]

urlpatterns += router.urls
