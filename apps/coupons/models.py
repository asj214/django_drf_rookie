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
    is_all_category = models.BooleanField('전체 카테고리 적용 여부', default=True)
    categories = models.JSONField('카테고리 아이디 list', default=None)
    is_all_product = models.BooleanField('전체 상품 적용 여부', default=True)
    products = models.JSONField('상품 아이디 list', default=None)
    is_active = models.BooleanField('사용 여부', default=False)

    class Meta:
        db_table = 'coupons'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['is_active', 'deleted_at',], name='active_coupons'),
        ]

    def __str__(self):
        return f'{self.id}'