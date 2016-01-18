# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_auto_20151230_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='japanese_center_skill',
        ),
        migrations.RemoveField(
            model_name='card',
            name='japanese_center_skill_details',
        ),
    ]
