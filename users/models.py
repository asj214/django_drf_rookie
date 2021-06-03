from uuid import uuid4
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from configs.models import BaseModel


class UserManager(BaseUserManager):

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(UserManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if not self.alive_only:
            return super().get_queryset()
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, name, password=None, **kwargs):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), name=name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(email=email, password=password, name=name, )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(
        verbose_name='Email address', max_length=255, unique=True,
    )
    name = models.CharField(verbose_name='name', max_length=30)
    is_active = models.BooleanField(verbose_name='Is active', default=True)
    access_token = models.UUIDField('access_token', default=uuid4, unique=True)
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    class Meta:
        db_table = 'users'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def generate_token(self):
        self.access_token = uuid4()
        self.save(update_fields=['access_token'])