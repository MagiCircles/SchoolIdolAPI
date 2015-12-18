# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_userpreferences_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='translated_collection',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='verified',
            field=models.PositiveIntegerField(default=0, verbose_name='Verified', choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, 'Bronze Verified')]),
            preserve_default=True,
        ),
    ]
