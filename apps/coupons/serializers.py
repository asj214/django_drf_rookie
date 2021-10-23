from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.categories.models import Category
from apps.categories.serializers import RelatedCategorySerializer
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    categories = RelatedCategorySerializer(many=True, read_only=True)
    name = serializers.CharField(max_length=255)
    is_fixed_discount = serializers.BooleanField(default=False)
    min_order_price = serializers.IntegerField(default=0)
    max_discount = serializers.IntegerField(default=0)
    is_all_category = serializers.BooleanField(default=True)
    is_all_product = serializers.BooleanField(default=True)
    is_active = serializers.BooleanField(default=False)


    class Meta:
        model = Coupon
        fields = (
            'id',
            'user',
            'name',
            'is_fixed_discount',
            'min_order_price',
            'max_discount',
            'is_all_category',
            'categories',
            'is_all_product',
            'products',
            'is_active',
            'expired_at',
            'created_at',
            'updated_at',
        )

    def add_categories(self, coupon: Coupon, categories: list = []):
        if not coupon.is_all_category and categories:
            coupon.categories.clear()
            for category in Category.objects.filter(id__in=categories).all():
                coupon.categories.add(category)
            coupon.save()
        return coupon

    def add_products(self, coupon: Coupon, products: list = []):
        if not coupon.is_all_product and products:
            coupon.products.clear()
            for product in Category.objects.filter(id__in=products).all():
                coupon.products.add(product)
            coupon.save()
        return coupon

    def create(self, validated_data):
        user = self.context.get('user')
        products = self.context.get('products')
        categories = self.context.get('categories')

        coupon = Coupon.objects.create(
            user=user,
            **validated_data
        )

        coupon = self.add_categories(coupon=coupon, categories=categories)
        coupon = self.add_products(coupon=coupon, products=products)
        
        return coupon
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)