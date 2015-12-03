# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_auto_20151202_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='message_data',
            field=models.CharField(max_length=1200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
