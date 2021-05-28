from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentListCreateView,
    CommentUpdateDestoryView
)


router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path(r'posts/<int:pk>/comments', CommentListCreateView.as_view()),
    path(r'posts/<int:pk>/comments/<int:comment_pk>', CommentUpdateDestoryView.as_view())
]

urlpatterns += router.urls
