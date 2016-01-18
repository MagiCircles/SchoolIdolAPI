# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_event_english_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='rank',
            new_name='number',
        ),
        migrations.AddField(
            model_name='activity',
            name='message_data',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='right_picture',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='right_picture_link',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(max_length=300, choices=[(b'Added a card', 'Added {} in {}'), (b'Idolized a card', 'Idolized {} in {}'), (b'Max Leveled a card', 'Max Leveled {} in {}'), (b'Max Bonded a card', 'Max Bonded {} in {}'), (b'Rank Up', 'Rank Up'), (b'Ranked in event', 'Ranked {} in event {} with score {}')]),
            preserve_default=True,
        ),
    ]
