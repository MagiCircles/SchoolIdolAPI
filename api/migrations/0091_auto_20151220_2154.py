# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_idol_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_idolized_url',
        ),
        migrations.RemoveField(
            model_name='card',
            name='card_url',
        ),
        migrations.RemoveField(
            model_name='card',
            name='round_card_url',
        ),
        migrations.AddField(
            model_name='card',
            name='total_owners',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='total_wishlist',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
