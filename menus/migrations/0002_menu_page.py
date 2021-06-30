# Generated by Django 3.2.3 on 2021-06-29 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_remove_page_menu'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='menu', to='pages.page'),
        ),
    ]