# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_auto_20150904_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='japan_only',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
