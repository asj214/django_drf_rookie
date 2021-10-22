from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryView
)


urlpatterns = [
    path(r'categories', CategoryListCreateView.as_view()),
    path(r'categories/<int:pk>', CategoryView.as_view()),
]
