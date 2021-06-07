from rest_framework import serializers
from .models import Comment
from customers.serializers import CustomerSerializer


class CommentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'customer',
            'commentable_id',
            'commentable_type',
            'body',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        user = self.context.get('user', None)
        parent = self.context.get('parent', None)
        return parent.comments.create(customer=user.customer, **validated_data)


class CommentableSerializer(serializers.Serializer):
    
    def comment_create(self, obj, validated_data):
        context = self.context
        context['parent'] = obj

        se = CommentSerializer(data=validated_data, context=context)
        se.is_valid(raise_exception=True)
        se.save()

        return obj