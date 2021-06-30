from rest_framework import serializers
from .models import Menu
from pages.serializers import PageSerializer


class MenuSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75)
    descr = serializers.CharField(max_length=75)
    order = serializers.IntegerField(default=0)
    is_published = serializers.BooleanField(default=False)
    page = PageSerializer()

    class Meta:
        model = Menu
        fields = ('id', 'parent', 'name', 'descr', 'order', 'page', 'is_published', 'created_at', 'updated_at')

    def create(self, validated_data):
        parent_id = self.context.get('parent_id', None)
        return Menu.objects.create(
            parent_id=parent_id,
            **validated_data
        )

    def update(self, obj, validated_data):
        parent_id = self.context.get('parent_id', None)
        for (key, value) in validated_data.items():
            setattr(obj, key, value)

        setattr(obj, 'parent_id', parent_id)

        obj.save()

        return obj
