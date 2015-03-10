# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20150308_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='japanese_name',
        ),
        migrations.AddField(
            model_name='idol',
            name='cv_instagram',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='cv_nickname',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='cv_twitter',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='cv_url',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
