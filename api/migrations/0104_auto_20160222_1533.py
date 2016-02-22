# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20160222_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='show_items',
            field=models.BooleanField(default=True, help_text='Should your items be visible to other players?', verbose_name=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='show_creation',
            field=models.BooleanField(default=True, help_text='Should this date be visible to other players?', verbose_name=b''),
            preserve_default=True,
        ),
    ]
