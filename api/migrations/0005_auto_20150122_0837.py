# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150122_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='beginning',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
