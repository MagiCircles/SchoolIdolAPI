# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0124_eventparticipation_account_owner_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='event',
            field=models.OneToOneField(related_name='song', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Event'),
            preserve_default=True,
        ),
    ]
