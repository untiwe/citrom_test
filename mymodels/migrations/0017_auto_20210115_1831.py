# Generated by Django 3.1.2 on 2021-01-15 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0016_auto_20210115_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='child_comment_id',
            new_name='perent_comment_id',
        ),
    ]