# Generated by Django 3.1.2 on 2021-01-15 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0015_auto_20210115_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='perent_comment_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='child_comment_id',
            field=models.ForeignKey(default=None, help_text='id "родительского" комментария, может быть пустым', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='mymodels.comments'),
        ),
    ]
