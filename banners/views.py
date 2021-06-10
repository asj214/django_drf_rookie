from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from configs.utils import set_context
from configs.permissions import StaffOnly, StaffOrReadOnly
from .models import BannerCategory, Banner
from .serializers import (
    BannerSerializer,
    BannerCategorySerializer
)


class BannerCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = BannerCategorySerializer
    queryset = BannerCategory.objects

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except BannerCategory.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'parent_id': request.data.pop('parent_id', None)}
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        banner_category = self.get_object(pk)
        context = {'parent_id': request.data.pop('parent_id', None)}

        serializer = self.serializer_class(
            banner_category,
            data=request.data,
            context=context,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        banner_category = self.get_object(pk)
        banner_category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BannerViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Banner.DoesNotExist:
            raise NotFound('Not Found')
    
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=set_context(request)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pass

    def update(self, request, pk=None, *args, **kwargs):
        pass

    def destroy(self, request, pk=None, *args, **kwargs):
        pass