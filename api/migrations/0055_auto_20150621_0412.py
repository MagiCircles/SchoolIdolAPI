# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20150419_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='verified',
            field=models.PositiveIntegerField(default=0, choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, b'')]),
            preserve_default=True,
        ),
    ]
