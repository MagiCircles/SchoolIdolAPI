# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0121_auto_20160331_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='center_alt_text',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='center_card_attribute',
            field=models.CharField(blank=True, max_length=6, null=True, choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='center_card_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='center_card_round_image',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='center_card_transparent_image',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
