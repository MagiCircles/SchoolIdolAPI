# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_auto_20160714_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='email_notifications_turned_off',
            field=models.CharField(max_length=15, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.PositiveIntegerField(choices=[(0, 'You have a new private message from {}.'), (1, '{} liked your activity.'), (2, '{} just followed you.')]),
            preserve_default=True,
        ),
    ]
