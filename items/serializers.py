from rest_framework import serializers
from .models import BaseItem, Option, Value


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = (
            'id',
            'option_id',
            'name',
            'created_at',
            'updated_at'
        )


class OptionSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, read_only=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'base_item_id',
            'name',
            'values',
            'created_at',
            'updated_at'
        )


class BaseItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    kind = serializers.CharField(max_length=24, default='general')
    is_active = serializers.BooleanField(default=False)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = BaseItem
        fields = (
            'id',
            'name',
            'kind',
            'options',
            'is_active',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        options = self.context.get('options', None)
        base_item = BaseItem.objects.create(**validated_data)

        if options:
            for opt in options:
                values = opt.pop('values', None)
                option = base_item.options.create(**opt)

                if values:
                    for val in values:
                        option.values.create(**val)

        return base_item