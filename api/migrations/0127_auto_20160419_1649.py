# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0126_account_owner_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='message_type',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Added a card'), (1, b'Idolized a card'), (2, b'Rank Up'), (3, b'Ranked in event'), (4, b'Verified'), (5, b'Trivia'), (6, b'Custom')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='creation',
            field=models.DateTimeField(auto_now=True, db_index=True),
            preserve_default=True,
        ),
    ]
