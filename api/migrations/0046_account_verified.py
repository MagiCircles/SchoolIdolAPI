# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20150403_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='verified',
            field=models.PositiveIntegerField(default=0, choices=[(0, b''), (1, 'Silver Verification (with screenshots)'), (2, 'Gold Verification (with transfer code)')]),
            preserve_default=True,
        ),
    ]
