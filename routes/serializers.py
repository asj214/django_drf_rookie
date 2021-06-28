from rest_framework import serializers
from .models import Route


class RouteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Route
        fields = ('id', 'parent', 'name', 'path', 'is_dynamic_component', 'component', 'depth', 'is_published', 'meta', 'created_at', 'updated_at')

    def create(self, validated_data):
        parent_id = self.context.get('parent_id', None)
        depth = self.set_depth(parent_id)

        return Route.objects.create(
            depth=depth,
            parent_id=parent_id,
            **validated_data
        )

    def update(self, obj, validated_data):
        parent_id = self.context.get('parent_id', None)
        depth = self.set_depth(parent_id)

        for (key, value) in validated_data.items():
            setattr(obj, key, value)

        setattr(obj, 'parent_id', parent_id)
        setattr(obj, 'depth', depth)

        obj.save()

        return obj

    def set_depth(self, parent_id=None):
        try:
            route = Route.objects.get(pk=parent_id)
            depth = route.depth + 1
        except Route.DoesNotExist:
            depth = 1
        return depth