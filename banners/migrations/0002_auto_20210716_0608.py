# Generated by Django 3.2.3 on 2021-07-16 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='mod_user',
            field=models.ForeignKey(db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mod_banners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='banner',
            name='user',
            field=models.ForeignKey(db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='banners', to=settings.AUTH_USER_MODEL),
        ),
    ]
