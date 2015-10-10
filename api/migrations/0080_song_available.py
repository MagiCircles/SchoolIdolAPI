# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='available',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
