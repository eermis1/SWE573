# Generated by Django 2.2.5 on 2019-12-07 15:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0016_auto_20191206_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='formfield',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
        ),
    ]
