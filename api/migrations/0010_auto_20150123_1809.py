# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_account_ownedcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='center',
            field=models.ForeignKey(blank=True, to='api.Card', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='friend_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='language',
            field=models.CharField(default=b'JP', max_length=10, choices=[(b'JP', b'Japanese'), (b'EN', b'English'), (b'KR', b'Korean'), (b'CH', b'Chinese')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='rank',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
