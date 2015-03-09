# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_idol_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='idol',
            field=models.ForeignKey(related_name='cards', blank=True, to='api.Idol', null=True),
            preserve_default=True,
        ),
    ]
