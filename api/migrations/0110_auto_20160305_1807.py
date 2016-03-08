# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_account_fake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationreport',
            name='comment',
            field=models.TextField(null=True, verbose_name='Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moderationreport',
            name='fake_eventparticipation',
            field=models.ForeignKey(related_name='moderationreport', on_delete=django.db.models.deletion.SET_NULL, to='api.EventParticipation', null=True),
            preserve_default=True,
        ),
    ]
