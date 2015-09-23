# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20150914_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='verified_by',
            field=models.ForeignKey(related_name='verificationsdone', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
