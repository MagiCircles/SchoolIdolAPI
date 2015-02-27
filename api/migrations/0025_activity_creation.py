# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20150227_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='creation',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.today, auto_now_add=True),
            preserve_default=False,
        ),
    ]
