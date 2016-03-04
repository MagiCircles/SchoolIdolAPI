# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0107_auto_20160303_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderationreport',
            name='moderation_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
