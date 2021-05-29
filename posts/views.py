from rest_framework import status, viewsets, generics
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

    def get_queryset(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request, pk=None, **kwargs):
        return Response({
            'pk': pk
        })

    def create(self, request, pk=None, **kwargs):

        context = set_context(request)

        try:
            context['post'] = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

        serializer = self.serializer_class(request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUpdateDestoryView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self, pk=None):
        pass

    def put(self, request, pk=None, **kwargs):
        pass

    def delete(self, request, pk=None, **kwargs):
        pass