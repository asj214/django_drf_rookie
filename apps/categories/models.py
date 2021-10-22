from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('childs').filter(deleted_at__isnull=True)


class Category(BaseModel, SoftDeleteModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        related_name='childs'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )
    name = models.CharField('카테고리명', max_length=256)
    depth = models.IntegerField('뎁스', default=0)
    order = models.IntegerField('정렬순위', default=0)
    is_active = models.BooleanField('사용 여부', default=False)

    objects = CategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['depth', 'order']
        indexes = []

    def __str__(self):
        return f'{self.id}'