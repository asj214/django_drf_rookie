from django.db import models
from configs.models import BaseModel, SoftDeleteModel


class Route(BaseModel, SoftDeleteModel):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='childrens'
    )
    path = models.CharField(verbose_name='path', max_length=75)
    name = models.CharField(verbose_name='name', max_length=75)
    is_dynamic_component = models.BooleanField('가변 컴포넌트 여부', default=False)
    component = models.CharField(verbose_name='components', max_length=125)
    meta = models.JSONField('route.meta', null=True, blank=True, default=None)
    depth = models.IntegerField(default=0)
    is_published = models.BooleanField('공개 여부', default=False)

    class Meta:
        db_table = 'routes'
        ordering = ['id', 'depth', 'created_at']
        indexes = [
            models.Index(fields=['deleted_at', 'is_published']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)