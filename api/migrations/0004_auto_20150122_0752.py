# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150122_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='japanese_name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
