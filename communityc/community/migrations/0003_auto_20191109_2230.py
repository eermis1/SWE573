# Generated by Django 2.2.5 on 2019-11-09 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20191109_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='community_rank',
            field=models.PositiveIntegerField(default=3, unique=True),
        ),
    ]
