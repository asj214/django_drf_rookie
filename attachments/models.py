from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from configs.models import BaseModel, SoftDeleteModel


class AttachmentManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(AttachmentManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Attachment(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='attachments'
    )

    attachmentable_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        db_column='attachmentable_type'
    )
    attachmentable_id = models.PositiveIntegerField(
        default=None,
        null=True,
        db_column='attachmentable_id'
    )
    content_object = GenericForeignKey('attachmentable_type', 'attachmentable_id')

    path = models.CharField(null=False, max_length=200)
    size = models.BigIntegerField(default=0)
    original = models.CharField(null=False, max_length=200)

    objects = AttachmentManager()

    class Meta:
        db_table = 'attachments'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at', 'attachmentable_id', 'attachmentable_type'], name='attachmentable'),
        ]

    def __str__(self):
        return '{}'.format(self.id)


class Attachmentable(models.Model):
    attachments = GenericRelation(
        'attachments.Attachment',
        default=None,
        null=True,
        object_id_field='attachmentable_id',
        content_type_field='attachmentable_type'
    )

    class Meta:
        abstract = True