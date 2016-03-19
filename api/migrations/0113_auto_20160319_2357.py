# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_auto_20160318_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='english_image',
            field=models.ImageField(null=True, upload_to=api.models.event_EN_upload_to, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='_staff_permissions',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
