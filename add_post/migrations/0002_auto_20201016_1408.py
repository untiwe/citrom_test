# Generated by Django 3.1.2 on 2020-10-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/'),
        ),
    ]
