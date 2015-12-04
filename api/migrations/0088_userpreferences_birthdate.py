# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_auto_20151203_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='birthdate',
            field=models.DateField(null=True, verbose_name='Birthdate', blank=True),
            preserve_default=True,
        ),
    ]
