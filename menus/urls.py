from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (MenuViewSet, MenuTreeView)


router = DefaultRouter(trailing_slash=False)
router.register(r'menus', MenuViewSet)

urlpatterns = [
    path(r'menus/tree', MenuTreeView.as_view()),
]

urlpatterns += router.urls
