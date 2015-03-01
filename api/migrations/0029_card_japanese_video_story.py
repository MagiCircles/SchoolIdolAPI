# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_activity_eventparticipation'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='japanese_video_story',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
    ]
