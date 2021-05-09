# Generated by Django 3.1.2 on 2021-02-19 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0017_auto_20210115_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewsPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_set', models.DateTimeField(auto_now_add=True, help_text='Дата просмотра')),
                ('post_id', models.ForeignKey(help_text='Связь, с постом, которому относится просмотри', on_delete=django.db.models.deletion.CASCADE, to='mymodels.posts')),
                ('user_id', models.ForeignKey(help_text='Связь с пользователем, который просмотрел', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]