# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150123_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedcard',
            name='owner_account',
            field=models.ForeignKey(related_name='ownedcard', default=1, to='api.Account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='center',
            field=models.ForeignKey(blank=True, to='api.OwnedCard', null=True),
            preserve_default=True,
        ),
    ]
