from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Page
from .serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PageSerializer
    queryset = Page.objects

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Page.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        page = self.get_object(pk)
        serializer = self.serializer_class(
            page,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        page = self.get_object(pk)
        page.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)