# Generated by Django 2.2.5 on 2019-11-24 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0012_remove_datastructure_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='additional_data_structure',
            field=models.ManyToManyField(to='community.DataStructure'),
        ),
    ]
