from rest_framework import serializers, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import BaseItem
from .serializers import BaseItemSerializer


class BaseItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = BaseItemSerializer
    queryset = BaseItem.objects.prefetch_related('options__values')

    def get_queryset(self):
        return self.queryset.all()

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except BaseItem.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'options': request.data.pop('options', None)
        }
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None, *args, **kwargs):
        item = self.get_object(pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
