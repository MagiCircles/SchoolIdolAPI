# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0123_auto_20160401_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipation',
            name='account_owner_status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Idol Supporter'), (b'LOVER', 'Idol Lover'), (b'AMBASSADOR', 'Idol Ambassador'), (b'PRODUCER', 'Idol Producer'), (b'DEVOTEE', 'Ultimate Idol Devotee')]),
            preserve_default=True,
        ),
    ]
