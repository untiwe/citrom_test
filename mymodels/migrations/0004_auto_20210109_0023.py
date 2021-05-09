# Generated by Django 3.1.2 on 2021-01-08 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0003_auto_20210105_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluationposts',
            old_name='ost_id',
            new_name='post_id',
        ),
        migrations.AlterField(
            model_name='adminmessages',
            name='date_create',
            field=models.DateField(auto_now_add=True, help_text='Дата создания'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='date_create',
            field=models.DateField(auto_now_add=True, help_text='Дата создания'),
        ),
        migrations.AlterField(
            model_name='commentsphotos',
            name='date_create',
            field=models.DateField(auto_now_add=True, help_text='Дата создания'),
        ),
        migrations.AlterField(
            model_name='commentsphotos',
            name='сomment_id',
            field=models.ForeignKey(default=None, help_text='Связь, с коментарием, которому пренадлежит фото', null=True, on_delete=django.db.models.deletion.CASCADE, to='mymodels.comments'),
        ),
        migrations.AlterField(
            model_name='evaluationcomments',
            name='date_set',
            field=models.DateField(auto_now_add=True, help_text='Дата оценки'),
        ),
        migrations.AlterField(
            model_name='evaluationposts',
            name='date_set',
            field=models.DateField(auto_now_add=True, help_text='Дата оценки'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_create',
            field=models.DateField(auto_now_add=True, help_text='Дата создания'),
        ),
        migrations.AlterField(
            model_name='postsphotos',
            name='date_create',
            field=models.DateField(auto_now_add=True, help_text='Дата создания'),
        ),
    ]
