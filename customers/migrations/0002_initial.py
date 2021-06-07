# Generated by Django 3.2.3 on 2021-06-03 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['user_id'], name='customers_user_id_5b5af9_idx'),
        ),
    ]
