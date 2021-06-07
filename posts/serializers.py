from rest_framework import serializers
from .models import Post
from customers.serializers import CustomerSerializer
from comments.serializers import CommentSerializer, CommentableSerializer


class PostSerializer(serializers.ModelSerializer, CommentableSerializer):
    customer = CustomerSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'customer',
            'title',
            'body',
            'created_at',
            'updated_at',
            'comments',
        )

    def create(self, validated_data):
        user = self.context.get('user', None)
        return Post.objects.create(customer=user.customer, **validated_data)
