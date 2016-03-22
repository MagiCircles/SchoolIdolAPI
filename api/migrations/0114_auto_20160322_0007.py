# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_auto_20160319_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='clean_ur',
            field=models.ImageField(null=True, upload_to=b'web/static/cards/ur_pairs/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='clean_ur_idolized',
            field=models.ImageField(null=True, upload_to=b'web/static/cards/ur_pairs/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='ur_pair',
            field=models.ForeignKey(related_name='other_ur_pair', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Card', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='ur_pair_idolized_reverse',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='ur_pair_reverse',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
