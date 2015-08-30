# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_activity_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='sub_unit',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_idolized_image',
            field=models.ImageField(null=True, upload_to=b'cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_image',
            field=models.ImageField(null=True, upload_to=b'cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='round_card_image',
            field=models.ImageField(null=True, upload_to=b'cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=b'events/', blank=True),
            preserve_default=True,
        ),
    ]
