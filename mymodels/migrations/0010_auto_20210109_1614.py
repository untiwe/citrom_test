# Generated by Django 3.1.2 on 2021-01-09 13:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0009_auto_20210109_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Дата создания'),
        ),
    ]
