from django.db import models
from configs.models import BaseModel, SoftDeleteModel


class BannerCategory(BaseModel, SoftDeleteModel):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='sub_categories'
    )
    name = models.CharField(verbose_name='name', max_length=75)
    depth = models.IntegerField(default=0)
    is_published = models.BooleanField('공개 여부', default=False)

    class Meta:
        db_table = 'banner_categories'
        ordering = ['id', 'depth', 'created_at']
        indexes = [
            models.Index(fields=['deleted_at', 'is_published']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class BannerManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(BannerManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset()

    def published(self):
        return self.filter(is_published=True)


class Banner(BaseModel, SoftDeleteModel):
    banner_category = models.ForeignKey(
        BannerCategory,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        related_name='banners'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None
    )
    title = models.CharField(verbose_name='배너명', max_length=75)
    link = models.CharField('클릭 시 이동할 페이지', null=True, blank=True, max_length=255)
    target = models.BooleanField('새창/페이지 이동 유무', default=False)
    order = models.IntegerField(default=0)
    image = models.CharField('이미지 경로', null=True, blank=True, max_length=255)
    started_at = models.DateTimeField('시작일', null=True)
    finished_at = models.DateTimeField('종료일', null=True)
    is_published = models.BooleanField('항상 노출 설정', default=False)

    objects = BannerManager()

    class Meta:
        db_table = 'banners'
        ordering = ['order', '-id']
        indexes = [
            models.Index(fields=['deleted_at', 'banner_category_id', 'started_at', 'finished_at', 'is_published']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.title)