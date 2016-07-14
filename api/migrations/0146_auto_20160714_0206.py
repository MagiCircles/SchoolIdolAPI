# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0145_auto_20160714_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreferences',
            name='has_unread_notifications',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='unread_notifications',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
