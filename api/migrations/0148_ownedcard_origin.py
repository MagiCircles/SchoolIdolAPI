# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0147_notification_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedcard',
            name='origin',
            field=models.PositiveIntegerField(null=True, choices=[(0, 'Honor Scouting (10+1, 50 love gems)'), (1, 'Solo Yolo (5 love gems)'), (5, 'Scouting Ticket'), (2, 'Vouchers (blue tickets)'), (3, 'Event Reward'), (4, 'Sticker Shop'), (6, 'At the end of a live')]),
            preserve_default=True,
        ),
    ]
