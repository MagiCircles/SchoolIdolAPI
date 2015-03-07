# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20150302_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='latitude',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='longitude',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
