# Generated by Django 3.2.3 on 2021-06-03 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=3, null=True, verbose_name='Country')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('is_advertising', models.BooleanField(default=False, verbose_name='광고수신')),
            ],
            options={
                'db_table': 'customers',
            },
        ),
    ]
