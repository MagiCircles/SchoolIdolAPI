# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_auto_20150914_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Rejected'), (1, b'Pending'), (2, b'In Progress'), (3, b'Verified')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='verification',
            field=models.PositiveIntegerField(default=1, verbose_name='Verification', choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, 'Bronze Verified')]),
            preserve_default=True,
        ),
    ]
