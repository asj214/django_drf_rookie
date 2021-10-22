from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import (
    CategorySerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('childs', 'user').all()

    def get_queryset(self):
        return self.queryset.filter(depth=1)
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'parent_id': request.data.get('parent_id')
        }

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('childs', 'user').all()

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound('Not Found')

    def get(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        serializer = self.serializer_class(category)

        return Response(serializer.data)
    
    def put(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        context = {
            'user': request.user,
            'parent_id': request.data.get('parent_id')
        }

        serializer = self.serializer_class(
            category,
            data=request.data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data) 
    
    def delete(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
