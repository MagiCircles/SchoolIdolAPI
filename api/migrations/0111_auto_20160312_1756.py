# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0110_auto_20160305_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='transparent_idolized_ur_pair',
        ),
        migrations.RemoveField(
            model_name='card',
            name='transparent_ur_pair',
        ),
    ]
