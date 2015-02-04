# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150122_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='promo_item',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateField(default=datetime.date(2013, 4, 16), null=True, blank=True),
            preserve_default=True,
        ),
    ]
