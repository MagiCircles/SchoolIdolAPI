# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0108_moderationreport_moderation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fake',
            field=models.BooleanField(default=False, verbose_name='Fake'),
            preserve_default=True,
        ),
    ]
