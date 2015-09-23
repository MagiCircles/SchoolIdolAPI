# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_auto_20150914_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='english_collection',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent_idolized_image',
            field=models.ImageField(null=True, upload_to=b'cards/transparent/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent_idolized_ur_pair',
            field=models.ImageField(null=True, upload_to=b'cards/transparent/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent_image',
            field=models.ImageField(null=True, upload_to=b'cards/transparent/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent_ur_pair',
            field=models.ImageField(null=True, upload_to=b'cards/transparent/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userimage',
            name='image',
            field=models.ImageField(null=True, upload_to=b'user_images/', blank=True),
            preserve_default=True,
        ),
    ]
