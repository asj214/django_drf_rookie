from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    BannerCategoryViewSet,
    BannerViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r'banner_categories', BannerCategoryViewSet)
router.register(r'backends/banners', BannerViewSet)

urlpatterns = []
urlpatterns += router.urls
