# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='friend_id',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='rank',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='transfer_code',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_idolized_url',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_url',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
