from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created_at', 'updated_at', 'comments')

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Post.objects.create(user=user, **validated_data)

    def comment_create(self, validated_data):
        return ''