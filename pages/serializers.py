from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75)
    path = serializers.CharField(max_length=75)

    class Meta:
        model = Page
        fields = ('id', 'name', 'path', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Page.objects.create(**validated_data)
