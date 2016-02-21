# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0100_auto_20160221_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='show_creation',
            field=models.BooleanField(default=False, help_text='Should this date be visible to other players?', verbose_name=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='show_friend_id',
            field=models.BooleanField(default=True, help_text='Should your friend ID be visible to other players?', verbose_name=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateField(help_text='When you started playing with this account.', null=True, verbose_name='Creation', blank=True),
            preserve_default=True,
        ),
    ]
