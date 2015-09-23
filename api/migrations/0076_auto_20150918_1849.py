# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_auto_20150917_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='verification_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
