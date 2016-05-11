# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_auto_20160419_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usicalvote',
            name='entry',
            field=models.PositiveIntegerField(default=0, choices=[(7, "\u10e6's \u262a\u2605\u266a"), (11, "\u03b2N's"), (13, 'FURious Alpaca'), (14, 'wAr-RICE'), (21, 'Crystal\u2756Lilies'), (22, 'Procrastinate \u2192 Tomorrow'), (23, 'Petit \u01b8\u04dc\u01b7 Papillon'), (38, '\u273f\u0187\u043d\u03c3c\u03c3\u2113\u03b1\u0442 \u0191\u03c3\u03b7\u2202\u03b1\u03b7\u0442\u273f'), (40, 'NYAvigators'), (54, '\u30dfk\u03bc'), (56, 'lilaq\u273f'), (57, 'Sock It 2 Me'), (59, '\u8336\u8336\u8336'), (61, 'AKB0033'), (62, 'Undefined Red'), (67, 'Midnight\u273fBlossoms')]),
            preserve_default=True,
        ),
    ]
