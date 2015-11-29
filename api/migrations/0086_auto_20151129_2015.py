# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0085_auto_20151125_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(max_length=300, choices=[(b'Added a card', 'Added {} in {}'), (b'Idolized a card', 'Idolized {} in {}'), (b'Max Leveled a card', 'Max Leveled {} in {}'), (b'Max Bonded a card', 'Max Bonded {} in {}'), (b'Rank Up', 'Rank Up {}'), (b'Ranked in event', 'Ranked {} in event {}')]),
            preserve_default=True,
        ),
    ]
