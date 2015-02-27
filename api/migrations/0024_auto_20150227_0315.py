# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='card',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='user',
        ),
        migrations.AddField(
            model_name='activity',
            name='account',
            field=models.ForeignKey(related_name='activities', blank=True, to='api.Account', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='ownedcard',
            field=models.ForeignKey(blank=True, to='api.OwnedCard', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='max_bond',
            field=models.BooleanField(default=False, verbose_name='Max Bonded (Kizuna)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='max_level',
            field=models.BooleanField(default=False, verbose_name='Max Leveled'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='stored',
            field=models.CharField(default=b'Deck', max_length=30, verbose_name='Stored', choices=[(b'Deck', 'Deck'), (b'Album', 'Album'), (b'Box', 'Present Box'), (b'Favorite', 'Wish List')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='best_girl',
            field=models.CharField(max_length=200, null=True, verbose_name='Best Girl', blank=True),
            preserve_default=True,
        ),
    ]
