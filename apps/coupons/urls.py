from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CouponViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r'coupons', CouponViewSet)

urlpatterns = []
urlpatterns += router.urls