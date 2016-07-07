# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_auto_20160707_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_idolized_image',
            field=models.ImageField(null=True, upload_to=b'c/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='card_image',
            field=models.ImageField(null=True, upload_to=b'c/', blank=True),
            preserve_default=True,
        ),
    ]
