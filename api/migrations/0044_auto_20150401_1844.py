# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20150316_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='english_t1_points',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_t1_rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_t2_points',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_t2_rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='japanese_t1_points',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='japanese_t1_rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='japanese_t2_points',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='japanese_t2_rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='account',
            field=models.ForeignKey(related_name='events', verbose_name='Account', to='api.Account'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='owner_account',
            field=models.ForeignKey(related_name='ownedcards', verbose_name='Account', to='api.Account'),
            preserve_default=True,
        ),
    ]
