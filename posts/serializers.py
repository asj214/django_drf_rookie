from rest_framework import serializers
from .models import Post
from users.serializers import RelatedUserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'body',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Post.objects.create(user=user, **validated_data)
