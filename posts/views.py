from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from configs.utils import set_context
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('user').all()

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=set_context(request))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(
            post,
            data=request.data,
            context=set_context(request),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
