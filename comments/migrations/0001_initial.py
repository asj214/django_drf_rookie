# Generated by Django 3.2.3 on 2021-05-28 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentable_type', models.ForeignKey(db_column='commentable_type', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('commentable_id', models.PositiveIntegerField(db_column='commentable_id', default=None, null=True)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'comments',
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['deleted_at', 'commentable_id', 'commentable_type'], name='commentable'),
        ),
    ]