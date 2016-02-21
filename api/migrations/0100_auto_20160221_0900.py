# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0099_auto_20160219_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateField(help_text='When you created this account.', null=True, verbose_name='Creation', blank=True),
            preserve_default=True,
        ),
    ]
