# Generated by Django 2.2.5 on 2019-11-09 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20191109_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='community_rank',
            field=models.IntegerField(default=3),
        ),
    ]
