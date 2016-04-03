# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0122_auto_20160331_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipation',
            name='account_language',
            field=models.CharField(default=b'JP', max_length=10, choices=[(b'JP', 'Japanese'), (b'EN', 'English'), (b'KR', 'Korean'), (b'CN', 'Chinese'), (b'TW', 'Taiwanese')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='account_link',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='account_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='account_owner',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='account_picture',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
