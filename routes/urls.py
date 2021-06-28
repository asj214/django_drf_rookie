from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (RouteViewSet)


router = DefaultRouter(trailing_slash=False)
router.register(r'routes', RouteViewSet)

urlpatterns = []
urlpatterns += router.urls
