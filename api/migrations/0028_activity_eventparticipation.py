# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20150227_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='eventparticipation',
            field=models.ForeignKey(blank=True, to='api.EventParticipation', null=True),
            preserve_default=True,
        ),
    ]
