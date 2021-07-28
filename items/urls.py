from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    BaseItemViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r'base_items', BaseItemViewSet)

urlpatterns = []
urlpatterns += router.urls
