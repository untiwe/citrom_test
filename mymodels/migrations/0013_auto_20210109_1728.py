# Generated by Django 3.1.2 on 2021-01-09 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymodels', '0012_auto_20210109_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsphotos',
            name='сomment_id',
            field=models.OneToOneField(default=None, help_text='Связь, с коментарием, которому пренадлежит фото', null=True, on_delete=django.db.models.deletion.CASCADE, to='mymodels.comments'),
        ),
    ]
