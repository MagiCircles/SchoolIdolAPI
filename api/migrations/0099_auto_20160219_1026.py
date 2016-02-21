# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_userpreferences_default_tab'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(help_text='When you created this account.', null=True, verbose_name='Creation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='starter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Card', help_text='The character that you selected when you started playing.', null=True, verbose_name='Starter'),
            preserve_default=True,
        ),
    ]
