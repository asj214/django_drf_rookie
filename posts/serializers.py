from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        post = Post.objects.create(user=user, **validated_data)
        return post