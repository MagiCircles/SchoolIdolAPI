# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_auto_20160105_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='main_unit',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
