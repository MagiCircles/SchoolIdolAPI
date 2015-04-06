# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20150406_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='accept_friend_requests',
            field=models.NullBooleanField(verbose_name='Accept friend requests'),
            preserve_default=True,
        ),
    ]
