# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20150701_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='status',
            field=models.CharField(max_length=12, null=True, choices=[(b'SUPPORTER', b'Idol Supporter'), (b'LOVER', b'Idol Lover'), (b'AMBASSADOR', b'Idol Ambassador'), (b'PRODUCER', b'Idol Producer'), (b'DEVOTEE', b'Ultimate Idol Devotee')]),
            preserve_default=True,
        ),
    ]
