# Generated by Django 3.1.7 on 2021-03-11 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0023_auto_20210311_1835'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeletedPosts',
            new_name='PostsDeleted',
        ),
    ]