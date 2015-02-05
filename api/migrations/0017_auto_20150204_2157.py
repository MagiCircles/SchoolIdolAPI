# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20150204_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_idolized_image',
            field=models.ImageField(null=True, upload_to=b'static/cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='card_image',
            field=models.ImageField(null=True, upload_to=b'static/cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='round_card_image',
            field=models.ImageField(null=True, upload_to=b'static/cards/', blank=True),
            preserve_default=True,
        ),
    ]
