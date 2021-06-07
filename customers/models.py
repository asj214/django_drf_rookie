from django.db import models


class CustomerManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(CustomerManager, self).__init__(*args, **kwargs)

    # def get_queryset(self):
    #     return super().get_queryset().select_related('user')
        # return super().get_queryset().prefetch_related('user')


class Customer(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        unique=True,
        related_name='customer'
    )
    country = models.CharField(
        "Country",
        max_length=3,
        null=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    is_advertising = models.BooleanField('광고수신', default=False)

    objects = CustomerManager()

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return '{}: {}'.format(self.id, self.nickname)