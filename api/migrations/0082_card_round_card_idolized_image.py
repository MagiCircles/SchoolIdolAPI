# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_song_itunes_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='round_card_idolized_image',
            field=models.ImageField(null=True, upload_to=b'cards/', blank=True),
            preserve_default=True,
        ),
    ]
