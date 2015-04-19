# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_ownedcard_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(max_length=300, choices=[(b'Added a card', 'Added a card'), (b'Idolized a card', 'Idolized a card'), (b'Max Leveled a card', 'Max Leveled a card'), (b'Max Bonded a card', 'Max Bonded a card'), (b'Rank Up', 'Rank Up'), (b'Ranked in event', 'Ranked in event')]),
            preserve_default=True,
        ),
    ]
