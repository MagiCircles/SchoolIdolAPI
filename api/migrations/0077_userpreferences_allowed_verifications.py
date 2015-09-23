# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_auto_20150918_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='allowed_verifications',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
