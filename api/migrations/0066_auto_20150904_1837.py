# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_auto_20150903_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='location',
            field=models.CharField(help_text='The city you live in. It might take up to 24 hours to update your location on the map.', max_length=200, null=True, verbose_name='Location', blank=True),
            preserve_default=True,
        ),
    ]
