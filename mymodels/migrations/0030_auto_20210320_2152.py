# Generated by Django 3.1.7 on 2021-03-20 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0029_auto_20210317_2325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(blank=True, default='', help_text='Автор поста', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=models.TextField(default='no', help_text='Контент поста', verbose_name='Контент'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='name',
            field=models.CharField(help_text='Название поста', max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_rating',
            field=models.IntegerField(default=0, help_text='Рейтинг поста', verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='views',
            field=models.IntegerField(default=0, help_text='Счеттчик просмотров', verbose_name='Просмотры'),
        ),
    ]
