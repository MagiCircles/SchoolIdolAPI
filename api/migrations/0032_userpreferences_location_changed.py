# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20150306_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='location_changed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
