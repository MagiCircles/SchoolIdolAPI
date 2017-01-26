# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0155_auto_20170120_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedcard',
            name='prefer_unidolized_image',
            field=models.BooleanField(default=False, verbose_name='Prefer unidolized card image'),
            preserve_default=True,
        ),
    ]
