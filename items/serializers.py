import json
from itertools import product
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
        options = self.context.pop('options')
        base_item = BaseItem.objects.create(**validated_data)

        for opt in options:
            values = opt.pop('values', [])
            option = base_item.options.create(**opt)

            for val in values:
                option.values.create(**val)

        self.create_items(base_item)
        return base_item
    
    def create_items(self, obj):

        results = []
        if obj.kind == 'general':
            results.append({
                'base_item_id': obj.id,
                'name': obj.name,
                'kind': obj.kind,
                'is_active': obj.is_active,
                'options': None,
                'created_at': str(obj.created_at),
                'updated_at': str(obj.updated_at)
            })
        else:
            options = obj.options.prefetch_related('values').all()
            opts = [[opt.id] for opt in options]

            values = []
            vals = []
            for opt in options:
                append = []
                for val in opt.values.all():
                    values.append(val)
                    append.append(val.id)
                vals.append(append)

            kinds = [list(product(opts[i], vals[i])) for i in range(len(opts))]

            for kind in product(*kinds):
                opt = []
                for r in kind:
                    option = next(filter(lambda x: x.id == r[0], options), None)
                    value = next(filter(lambda x: x.id == r[1], values), None)

                    opt.append({
                        'option_id': option.id,
                        'option_name': option.name,
                        'value_id': value.id,
                        'value_name': value.name
                    })

                results.append({
                    'base_item_id': obj.id,
                    'name': obj.name,
                    'kind': obj.kind,
                    'is_active': obj.is_active,
                    'options': opt,
                    'created_at': str(obj.created_at),
                    'updated_at': str(obj.updated_at)
                })

        print(json.dumps(results, indent=2))
        # Item.objects.bulk_create(results) 