from django.db import models
from configs.models import BaseModel, SoftDeleteModel


class Menu(BaseModel, SoftDeleteModel):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='childs'
    )
    name = models.CharField(verbose_name='name', max_length=75)
    descr = models.CharField(verbose_name='메뉴 설명', max_length=75)
    depth = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    page = models.ForeignKey(
        'pages.Page',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='menu'
    )
    is_published = models.BooleanField('공개 여부', default=False)

    class Meta:
        db_table = 'menus'
        ordering = ['id', 'depth', 'created_at']
        indexes = [
            models.Index(fields=['deleted_at', 'is_published']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)