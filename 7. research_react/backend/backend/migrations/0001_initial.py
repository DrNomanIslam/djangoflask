# Generated by Django 4.1.2 on 2022-10-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.CharField(default='', max_length=10)),
                ('first_name', models.CharField(default='', max_length=10)),
                ('last_name', models.CharField(default='', max_length=10)),
                ('email', models.EmailField(default='', max_length=40)),
                ('highest_qualification', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('journal', models.CharField(max_length=50)),
                ('year_of_publication', models.IntegerField(default=2022)),
                ('volume', models.IntegerField(default=1)),
                ('issue', models.IntegerField(default=1)),
                ('pp', models.CharField(max_length=15)),
                ('authors', models.ManyToManyField(to='backend.author')),
            ],
        ),
    ]
