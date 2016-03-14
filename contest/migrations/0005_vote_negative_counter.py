# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20160311_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='negative_counter',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
