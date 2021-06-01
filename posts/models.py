from django.db import models
from configs.models import BaseModel, SoftDeleteModel
from comments.models import Commentable


class PostQuerySet(models.QuerySet):

    def relations(self):
        return self.prefetch_related('user', 'comments')


class Post(Commentable, BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False
    )
    title = models.CharField(verbose_name='title', max_length=75)
    body = models.TextField()

    objects = PostQuerySet.as_manager()

    class Meta:
        db_table = 'posts'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.title)