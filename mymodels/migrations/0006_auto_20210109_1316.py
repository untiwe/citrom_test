# Generated by Django 3.1.2 on 2021-01-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0005_auto_20210109_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='perent_comment_id',
            field=models.IntegerField(default='', help_text='id "родительского" комментария, может быть пустым', null=True),
        ),
    ]
