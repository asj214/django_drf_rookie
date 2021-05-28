from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'commentable_id', 'commentable_type', 'body', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Comment.objects.create(user=user, **validated_data)
