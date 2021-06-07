from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from configs.models import BaseModel, SoftDeleteModel


class CommentManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(CommentManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Comment(BaseModel, SoftDeleteModel):
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='comments'
    )

    commentable_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        db_column='commentable_type'
    )
    commentable_id = models.PositiveIntegerField(
        default=None,
        null=True,
        db_column='commentable_id'
    )
    content_object = GenericForeignKey('commentable_type', 'commentable_id')

    body = models.TextField(null=False)

    objects = CommentManager()

    class Meta:
        db_table = 'comments'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at', 'commentable_id', 'commentable_type'], name='commentable'),
        ]

    def __str__(self):
        return '{}'.format(self.id)


class Commentable(models.Model):
    comments = GenericRelation(
        'comments.Comment',
        default=None,
        null=True,
        object_id_field='commentable_id',
        content_type_field='commentable_type'
    )

    class Meta:
        abstract = True
