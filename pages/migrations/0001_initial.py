# Generated by Django 3.2.3 on 2021-06-29 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='name')),
                ('path', models.CharField(max_length=75, verbose_name='path')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'pages',
                'ordering': ['id'],
            },
        ),
        migrations.AddIndex(
            model_name='page',
            index=models.Index(fields=['deleted_at'], name='pages_deleted_df2f99_idx'),
        ),
    ]