from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'email',
            'name',
            'nickname',
            'phone',
            'country',
            'last_login',
            'is_active',
            'is_advertising',
            'created_at'
        ]

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Customer.objects.create(user=user, **validated_data)
        # return user.customer.create(**validated_data)