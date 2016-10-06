# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0152_activity_hot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipation',
            name='account_owner_status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Idol Supporter'), (b'LOVER', 'Idol Lover'), (b'AMBASSADOR', 'Idol Ambassador'), (b'PRODUCER', 'Idol Producer'), (b'DEVOTEE', 'Ultimate Idol Devotee'), (b'STAFF', 'Staff'), (b'DATABASE', 'Database Maintainer')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='origin',
            field=models.PositiveIntegerField(null=True, choices=[(0, 'Honor Scouting (10+1, 50 love gems)'), (1, 'Solo Yolo (5 love gems)'), (5, 'Scouting Ticket'), (2, 'Vouchers (blue tickets)'), (3, 'Event Reward'), (4, 'Sticker Shop'), (6, 'At the end of a live'), (7, 'Regular Scouting (with friend points)'), (8, 'Login Bonus')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Idol Supporter'), (b'LOVER', 'Idol Lover'), (b'AMBASSADOR', 'Idol Ambassador'), (b'PRODUCER', 'Idol Producer'), (b'DEVOTEE', 'Ultimate Idol Devotee'), (b'STAFF', 'Staff'), (b'DATABASE', 'Database Maintainer')]),
            preserve_default=True,
        ),
    ]
