from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class Product(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )
    name = models.CharField('상품명', max_length=256)
    categories = models.ManyToManyField(
        'categories.Category',
        related_name='products',
        db_constraint=False,
    )
    price = models.BigIntegerField('상품 가격', null=True, default=0)
    description = models.CharField('상품 상세', max_length=256)
    is_active = models.BooleanField('사용 여부', default=False)
    is_published = models.BooleanField('전시 여부', default=False)

    class Meta:
        db_table = 'products'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['is_active', 'deleted_at',], name='active_products'),
            models.Index(fields=['is_active', 'is_published', 'deleted_at',], name='publish_products'),
        ]

    def __str__(self):
        return f'{self.id}'