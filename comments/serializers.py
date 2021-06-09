from rest_framework import serializers
from .models import Comment
from users.serializers import NestedUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'commentable_id',
            'commentable_type',
            'body',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'commentable_id': {'write_only': True},
            'commentable_type': {'write_only': True}
        }


    def create(self, validated_data):
        user = self.context.get('user', None)
        parent = self.context.get('parent', None)
        return parent.comments.create(user=user, **validated_data)


class CommentableSerializer(serializers.Serializer):
    
    def comment_create(self, obj, validated_data):
        context = self.context
        context['parent'] = obj

        se = CommentSerializer(data=validated_data, context=context)
        se.is_valid(raise_exception=True)
        se.save()

        return obj