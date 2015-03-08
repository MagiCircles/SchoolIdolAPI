# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_idol_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='main',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
