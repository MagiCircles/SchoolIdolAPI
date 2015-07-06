# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_auto_20150704_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='donation_link',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='donation_link_title',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Idol Supporter'), (b'LOVER', 'Idol Lover'), (b'AMBASSADOR', 'Idol Ambassador'), (b'PRODUCER', 'Idol Producer'), (b'DEVOTEE', 'Ultimate Idol Devotee')]),
            preserve_default=True,
        ),
    ]
