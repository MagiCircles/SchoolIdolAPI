# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0151_auto_20160905_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='hot',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
