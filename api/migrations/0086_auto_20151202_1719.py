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
            name='creation',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(max_length=300, choices=[(b'Added a card', 'Added {} in {}'), (b'Idolized a card', 'Idolized {} in {}'), (b'Rank Up', 'Rank Up {}'), (b'Ranked in event', 'Ranked {} in event {}'), (b'Verified', 'Just got verified: {}'), (b'Custom', b'Custom')]),
            preserve_default=True,
        ),
    ]
