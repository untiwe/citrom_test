# Generated by Django 3.1.2 on 2021-01-09 13:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0010_auto_20210109_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 9, 13, 15, 24, 404900, tzinfo=utc), help_text='Дата создания'),
        ),
    ]
