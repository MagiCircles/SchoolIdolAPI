# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_card_round_card_idolized_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='english_image',
            field=models.ImageField(null=True, upload_to=b'events/EN/', blank=True),
            preserve_default=True,
        ),
    ]
