# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0148_ownedcard_origin'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='invalid_email',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
