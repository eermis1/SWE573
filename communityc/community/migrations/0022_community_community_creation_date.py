# Generated by Django 2.2.5 on 2019-12-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0021_auto_20191213_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='community_creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
