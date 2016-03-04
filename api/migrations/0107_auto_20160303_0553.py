# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_moderationreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationreport',
            name='fake_account',
            field=models.ForeignKey(related_name='moderationreport', to='api.Account', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moderationreport',
            name='fake_eventparticipation',
            field=models.ForeignKey(related_name='moderationreport', to='api.EventParticipation', null=True),
            preserve_default=True,
        ),
    ]
