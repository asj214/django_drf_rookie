from functools import partial
from rest_framework import serializers, status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from configs.utils import set_context
from .models import Post
from .serializers import PostSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.relations().all()

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


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self, pk=None):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post.comments, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

        serializer = PostSerializer(post, context=set_context(request))
        serializer.comment_create(post, request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUpdateDestoryView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects

    def get_object(self, pk=None, id=None):
        try:
            post = Post.objects.get(pk=pk)
            comment = post.comments.get(pk=id)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

        return post, comment

    def put(self, request, pk=None, id=None, **kwargs):

        post, comment = self.get_object(pk, id)

        serializer = self.serializer_class(
            comment,
            data=request.data,
            partial=True,
            context=set_context(request)
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        se = PostSerializer(post)
        return Response(se.data)

    def delete(self, request, pk=None, id=None, **kwargs):
        post, comment = self.get_object(pk, id)
        comment.delete()

        serializer = PostSerializer(post)
        return Response(serializer.data)