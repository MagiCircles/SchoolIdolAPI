# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0131_auto_20160519_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='other_event',
            field=models.ForeignKey(related_name='other_cards', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='other_event_english_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='other_event_image',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='other_event_japanese_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
