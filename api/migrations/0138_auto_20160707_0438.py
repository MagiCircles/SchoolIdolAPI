# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0137_auto_20160707_0257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='card_idolized_image',
            new_name='english_card_idolized_image',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='card_image',
            new_name='english_card_image',
        ),
        migrations.AddField(
            model_name='card',
            name='game_id',
            field=models.PositiveIntegerField(unique=True, null=True),
            preserve_default=True,
        ),
    ]
