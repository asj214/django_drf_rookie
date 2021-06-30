from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PageViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'pages', PageViewSet)

urlpatterns = []
urlpatterns += router.urls
