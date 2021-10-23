from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class Coupon(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )
    name = models.CharField('쿠폰명', max_length=256)
    is_fixed_discount = models.BooleanField('고정할인 여부', default=False)
    min_order_price = models.BigIntegerField('최소 주문 금액', null=True, default=0)
    max_discount = models.BigIntegerField('최대 할인 금액', null=True, default=0)
    expired_at = models.DateTimeField('만료일', null=True,)
    ignore_categories = models.ManyToManyField(
        'categories.Category',
        related_name='ignore_coupons',
        db_constraint=False,
    )

    class Meta:
        db_table = 'coupons'
        ordering = ['-id']
        indexes = []

    def __str__(self):
        return f'{self.id}'