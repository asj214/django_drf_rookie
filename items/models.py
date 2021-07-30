from django.db import models
from configs.models import BaseModel, SoftDeleteModel


class BaseItem(BaseModel, SoftDeleteModel):
    name = models.CharField('상품명', max_length=256)
    kind = models.CharField('구분', max_length=24, default='general')
    is_active = models.BooleanField('활성 여부', default=False)

    class Meta:
        db_table = 'base_items'
        ordering = ['-id']
        indexes = []

    def __str__(self):
        return f'{self.id}'


class Option(BaseModel):
    base_item = models.ForeignKey(
        'items.BaseItem',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='options'
    )
    name = models.CharField('상품명', max_length=256)

    class Meta:
        db_table = 'options'
        ordering = ['base_item_id', 'id']

    def __str__(self):
        return f'{self.id}'


class Value(BaseModel):
    option = models.ForeignKey(
        'items.Option',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='values'
    )
    name = models.CharField('옵션 값', max_length=256)

    class Meta:
        db_table = 'values'
        ordering = ['option_id', 'id']

    def __str__(self):
        return f'{self.id}'


'''
class Item(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'items'
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}: {self.name}'
'''