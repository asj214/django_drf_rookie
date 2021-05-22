from django.urls import path
from .views import InitView

urlpatterns = [
    path(r'init', InitView.as_view()),
]
