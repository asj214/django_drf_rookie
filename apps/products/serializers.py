from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.categories.serializers import RelatedCategorySerializer
from apps.categories.models import Category
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    price = serializers.IntegerField(default=0)
    description = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=False)
    is_published = serializers.BooleanField(default=False)
    user = UserSerializer(read_only=True)
    categories = RelatedCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'categories',
            'user',
            'name',
            'price',
            'description',
            'is_active',
            'is_published',
            'created_at',
            'updated_at',
        )
    
    def create(self, validated_data):
        user = self.context.get('user')
        categories = self.context.get('categories')

        product = Product.objects.create(
            user=user,
            **validated_data
        )

        if categories:
            product.categories.clear()
            for category in Category.objects.filter(id__in=categories).all():
                product.categories.add(category)
            product.save()
        return product