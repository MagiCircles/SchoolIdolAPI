# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0091_auto_20151220_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='ranking_attribute',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='ranking_rarity',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='ranking_special',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='stored',
            field=models.CharField(default=b'Deck', max_length=30, verbose_name='Stored', choices=[(b'Deck', 'Deck (You have it)'), (b'Album', "Album (You don't have it anymore)"), (b'Box', 'Present Box'), (b'Favorite', 'Wish List')]),
            preserve_default=True,
        ),
    ]
