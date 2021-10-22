from rest_framework import serializers
from conf.serializers import RecursiveField
from apps.users.serializers import UserSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    depth = serializers.IntegerField(min_value=1, max_value=3)
    order = serializers.IntegerField(default=1)
    is_active = serializers.BooleanField(default=False)
    children = RecursiveField(many=True, read_only=True, source='childs')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'parent_id',
            'user',
            'name',
            'depth',
            'order',
            'is_active',
            'created_at',
            'updated_at',
            'children'
        )

    def create(self, validated_data):
        user = self.context.get('user')
        parent_id = self.context.get('parent_id')

        return Category.objects.create(
            parent_id=parent_id,
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):
        user = self.context.get('user')
        parent_id = self.context.get('parent_id')

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.parent_id = parent_id
        instance.user = user
        instance.save()

        return instance