from django.conf import settings
from rest_framework import serializers
from configs.utils import upload_files
from configs.exceptions import AttachmentUploadError
from .models import BannerCategory, Banner
from users.serializers import NestedUserSerializer



UPLOAD_DIR = '{0}/{1}'.format(settings.BASE_UPLOAD_PATH, 'banners')

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
    link = serializers.URLField(default=None)
    order = serializers.IntegerField(default=1)
    target = serializers.BooleanField(default=False)
    image = serializers.SerializerMethodField()
    started_at = serializers.DateTimeField(default=None)
    finished_at = serializers.DateTimeField(default=None)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Banner
        fields = (
            'id',
            'banner_category',
            'user',
            'image',
            'order',
            'link',
            'target',
            'title',
            'started_at',
            'finished_at',
            'is_published',
            'created_at',
            'updated_at'
        )
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        request = self.context.get('request')
        banner_category_id = request.data.get('banner_category_id')

        banner = Banner.objects.create(
            user=user,
            banner_category_id=banner_category_id,
            **validated_data
        )

        upfile = request.FILES.get('upfile', None)
        if upfile is not None:
            res = upload_files(upfile, UPLOAD_DIR)
            if not res:
                raise AttachmentUploadError
            banner.image = res.get('path')
            banner.save()

        return banner
    
    def get_image(self, obj):
        return '{0}/{1}'.format(settings.BASE_URL, obj.image)
