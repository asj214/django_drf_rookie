from rest_framework import serializers
from .models import Post
from users.serializers import NestedUserSerializer
from comments.serializers import CommentSerializer, CommentableSerializer


class PostSerializer(serializers.ModelSerializer, CommentableSerializer):
    user = NestedUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'body',
            'created_at',
            'updated_at',
            'comments',
        )

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Post.objects.create(user=user, **validated_data)
