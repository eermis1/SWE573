# Generated by Django 2.2.5 on 2019-12-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0017_post_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='community_tag_wiki',
            field=models.CharField(default=1, max_length=400),
            preserve_default=False,
        ),
    ]
