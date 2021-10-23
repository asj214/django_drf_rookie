from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Coupon
from .serializers import (
    CouponSerializer,
)


class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CouponSerializer
    queryset = Coupon.objects.prefetch_related('user', 'categories', 'products').all()

    def get_queryset(self):
        return self.queryset
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Coupon.DoesNotExist:
            raise NotFound('Not Found')
    
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'categories': request.data.pop('categories', []),
            'products': request.data.pop('products', [])
        }

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        coupon = self.get_object(pk)
        serializer = self.serializer_class(coupon)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        coupon = self.get_object(pk)
        context = {
            'user': request.user,
            'categories': request.data.pop('categories', []),
            'products': request.data.pop('products', [])
        }
        serializer = self.serializer_class(
            coupon,
            data=request.data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        coupon = self.get_object(pk)
        coupon.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)