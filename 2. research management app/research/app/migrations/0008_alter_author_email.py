# Generated by Django 3.2.13 on 2022-06-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20220616_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(default='', max_length=20),
        ),
    ]
