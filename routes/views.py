from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Route
from .serializers import RouteSerializer


class RouteViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RouteSerializer
    queryset = Route.objects

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Route.DoesNotExist:
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