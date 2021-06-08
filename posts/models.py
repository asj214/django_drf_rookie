from django.db import models
from configs.models import BaseModel, SoftDeleteModel
from comments.models import Commentable


class PostManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(PostManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().prefetch_related('user', 'comments__user')


class Post(Commentable, BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='posts'
    )
    title = models.CharField(verbose_name='title', max_length=75)
    body = models.TextField()

    objects = PostManager()

    class Meta:
        db_table = 'posts'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.title)