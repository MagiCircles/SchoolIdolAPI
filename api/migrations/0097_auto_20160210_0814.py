# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_idol_main_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='message_data',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
