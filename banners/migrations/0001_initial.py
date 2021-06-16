# Generated by Django 3.2.3 on 2021-06-09 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_categories', to='banners.bannercategory')),
                ('name', models.CharField(max_length=75, verbose_name='name')),
                ('depth', models.IntegerField(default=0)),
                ('is_published', models.BooleanField(default=False, verbose_name='공개 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'banner_categories',
                'ordering': ['id', 'depth', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_category', models.ForeignKey(db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='banners', to='banners.bannercategory')),
                ('user', models.ForeignKey(db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('title', models.CharField(max_length=75, verbose_name='배너명')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='클릭 시 이동할 페이지')),
                ('target', models.BooleanField(default=False, verbose_name='새창/페이지 이동 유무')),
                ('order', models.IntegerField(default=0)),
                ('image', models.CharField(blank=True, max_length=255, null=True, verbose_name='이미지 경로')),
                ('started_at', models.DateTimeField(null=True, verbose_name='시작일')),
                ('finished_at', models.DateTimeField(null=True, verbose_name='종료일')),
                ('is_published', models.BooleanField(default=False, verbose_name='항상 노출 설정')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'banners',
                'ordering': ['order', '-id'],
            },
        ),
        migrations.AddIndex(
            model_name='bannercategory',
            index=models.Index(fields=['deleted_at', 'is_published'], name='banner_cate_deleted_8324eb_idx'),
        ),
        migrations.AddIndex(
            model_name='banner',
            index=models.Index(fields=['deleted_at', 'banner_category_id', 'started_at', 'finished_at', 'is_published'], name='banners_deleted_e83544_idx'),
        ),
    ]