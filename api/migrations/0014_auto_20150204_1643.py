# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150204_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hp',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
