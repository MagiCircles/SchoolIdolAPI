# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20160621_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ownedcard',
            field=models.ForeignKey(related_name='members', to='api.OwnedCard'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usicalvote',
            name='entry',
            field=models.PositiveIntegerField(default=0, choices=[(7, "\u10e6's \u262a\u2605\u266a"), (13, 'FURious Alpaca'), (14, 'wAr-RICE'), (54, '\u30dfk\u03bc'), (56, 'lilaq\u273f'), (59, '\u8336\u8336\u8336')]),
            preserve_default=True,
        ),
    ]
