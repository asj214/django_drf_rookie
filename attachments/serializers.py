from django.conf import settings
from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    path = serializers.CharField()
    original = serializers.CharField()
    # url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = (
            'id',
            'attachmentable_type',
            'attachmentable_id',
            'name',
            'path',
            # 'url'
        )
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        attachment = Attachment.objects.create(user=user, **validated_data)
        return attachment
    
    # def get_url(self, obj):
    #     return '{0}/{1}'.format(settings.BASE_URL, obj.path)