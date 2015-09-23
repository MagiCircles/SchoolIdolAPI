# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_auto_20150914_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='verification_comment',
            field=models.TextField(null=True, verbose_name='Comment', blank=True),
            preserve_default=True,
        ),
    ]
