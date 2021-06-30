from django.db import models
from configs.models import BaseModel, SoftDeleteModel


class Page(BaseModel, SoftDeleteModel):
    name = models.CharField(verbose_name='name', max_length=75)
    path = models.CharField(verbose_name='path', max_length=75)

    class Meta:
        db_table = 'pages'
        ordering = ['id']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)