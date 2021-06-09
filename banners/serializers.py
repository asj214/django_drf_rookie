from rest_framework import serializers
from .models import BannerCategory, Banner
from users.serializers import NestedUserSerializer


class BannerCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = BannerCategory
        fields = ('id', 'parent', 'depth', 'name', 'is_published', 'created_at', 'updated_at')
        extra_kwargs = {
            'user': {'write_only': True},
        }

    def create(self, validated_data):
        parent_id = self.context.get('parent_id', None)
        depth = self.set_depth(parent_id)

        return BannerCategory.objects.create(
            depth=depth,
            parent_id=parent_id,
            **validated_data
        )

    def update(self, obj, validated_data):
        parent_id = self.context.get('parent_id', None)
        depth = self.set_depth(parent_id)

        print('### parent_id: ', parent_id)

        for (key, value) in validated_data.items():
            setattr(obj, key, value)

        setattr(obj, 'parent_id', parent_id)
        setattr(obj, 'depth', depth)

        obj.save()

        return obj

    def set_depth(self, parent_id=None):
        try:
            banner_category = BannerCategory.objects.get(pk=parent_id)
            depth = banner_category.depth + 1
        except BannerCategory.DoesNotExist:
            depth = 1
        return depth


class BannerSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)
    title = serializers.CharField(max_length=75)
    order = serializers.IntegerField(default=1)
    started_at = serializers.DateTimeField(default=None)
    finished_at = serializers.DateTimeField(default=None)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Banner
        fields = (
            'id',
            'banner_category',
            'user',
            'title',
            'link',
            'target',
            'order',
            'image',
            'started_at',
            'finished_at',
            'is_published',
            'created_at',
            'updated_at'
        )
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        return Banner.objects.create(user=user, **validated_data)
