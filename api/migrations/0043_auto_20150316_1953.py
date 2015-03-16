# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20150315_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.OwnedCard', help_text='The character that talks to you on your home screen.', null=True, verbose_name='Center'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='event',
            field=models.ForeignKey(related_name='cards', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Event', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='idol',
            field=models.ForeignKey(related_name='cards', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Idol', null=True),
            preserve_default=True,
        ),
    ]
