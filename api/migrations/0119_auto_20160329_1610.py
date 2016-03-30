# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0118_usicalvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usicalvote',
            name='entry',
            field=models.PositiveIntegerField(default=0, choices=[(2, '\u300c\u0442 \u043d \u03ad \u0430 \u2606\u300d'), (5, 'CELESTIC\u2600SMILE'), (7, "\u10e6's \u262a\u2605\u266a"), (9, '\xd0-SEND'), (10, 'a i r i \u266b~'), (11, "\u03b2N's"), (13, 'FURious Alpaca'), (14, 'wAr-RICE'), (16, 'Fruits\u2729Idols'), (17, '\u5922\u898b\u308b10\u5b50'), (18, '\u2727Sweet PaniQ\u2727'), (19, '\xb5nit'), (21, 'Crystal\u2756Lilies'), (22, 'Procrastinate \u2192 Tomorrow'), (23, 'Petit \u01b8\u04dc\u01b7 Papillon'), (24, '\u300e NeoN \u2606 MIDNIGHT\u300f'), (30, 'three oppais \u2764'), (31, 'Kuma Harmony'), (32, 'Apple \u03c0'), (35, 'Puresmile'), (38, '\u273f\u0187\u043d\u03c3c\u03c3\u2113\u03b1\u0442 \u0191\u03c3\u03b7\u2202\u03b1\u03b7\u0442\u273f'), (39, 'First Live!'), (40, 'NYAvigators'), (42, '\u03ac\u03bb\u03c4\u03bfs'), (45, 'SweeTea \u01b8\u04dc\u01b7'), (46, 'Paper\u2661Heart'), (49, '\u2746Ne\u03b1polit\u03b1n\u2746'), (51, '\u029a Little Wings \u025e'), (52, 'l\u039bmid\u039b'), (53, "\u03bc'sketeers"), (54, '\u30dfk\u03bc'), (56, 'lilaq\u273f'), (57, 'Sock It 2 Me'), (59, '\u8336\u8336\u8336'), (61, 'AKB0033'), (62, 'Undefined Red'), (63, 'This Mystery'), (64, "No \u03bc's No life"), (67, 'Midnight\u273fBlossoms')]),
            preserve_default=True,
        ),
    ]
